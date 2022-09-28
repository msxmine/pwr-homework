with Ada.Text_IO; use Ada.Text_IO;
with Ada.Containers.Vectors;
with Ada.Strings.Fixed;
with Ada.Numerics.Discrete_Random;
with Ada.Numerics.Float_Random;

procedure z1 is
    NumNodes : constant Integer := 10;
    NumShortcuts : Integer := 5;
    NumPackets : constant Integer := 6;
    NumBackPaths : Integer := 7;
    NumMaxHops : constant Integer := 15;
    RandomMillisLimit : constant Integer := 1000;


    task type main is
        entry Wat;
    end main;
    type Ptr_Main is access main;
    Prog : Ptr_Main;

    task type DeadCounter (PakCnt : Integer) is
        entry Count;
    end DeadCounter;
    task body DeadCounter is
        DeadNum : Integer;
    begin
        DeadNum := 0;
        while DeadNum < PakCnt loop
            accept Count;
            DeadNum := DeadNum+1;
        end loop;
        Prog.Wat;
    end DeadCounter;

    type Ptr_Deadcnt is access DeadCounter;
    Dcnt : Ptr_Deadcnt;
    
    function Itoa(I : Integer) return String is
    begin
        return Ada.Strings.Fixed.Trim(Integer'Image(I), Ada.Strings.Left);
    end Itoa;

    FloatGen : Ada.Numerics.Float_Random.Generator;
    function RandomIdx(last: Integer) return Integer is
        gentmp : Float;
        protmp: Integer;
    begin
        gentmp := Ada.Numerics.Float_Random.Random(FloatGen) * Float(last);
        protmp := Natural(Float'Rounding(gentmp));
        if protmp = last then
            protmp := 0;
        end if;
        return protmp;
    end RandomIdx;

    type randRange is range 0..RandomMillisLimit;
    package Rand_Int is new Ada.Numerics.Discrete_Random(randRange);
    RandomGen : Rand_Int.Generator;
    procedure RandomDelay is
        generated : randRange;
        waited : Duration;
    begin
        generated := Rand_Int.random(RandomGen);
        waited := Duration(generated) / 1000.0;
        delay waited;
    end;
    
    package Integer_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => Integer);
    type Packet is record
        Num : Integer;
        Path : Integer_Vectors.Vector;
        Ttl : Integer;
        Dead : Integer;
    end record;
    type PacketPointer is access all Packet;
    type Node is record
        Id : Integer;
        Exits : Integer_Vectors.Vector;
        Handled : Integer_Vectors.Vector;
        Traps : Integer;
    end record;
    type NodePointer is access all Node;
    type NodeArray is array (Natural range <>) of aliased Node;
    Graph : NodeArray (0 .. NumNodes-1);

    task Printer is
        entry Print(line : String);
    end Printer;
    task body Printer is
        Ended : Integer;
    begin
        Ended := 0;
        loop
            accept Print(line : String) do
                if line = "" then
                    Ended := 1;
                else
                    Put_Line(line);
                end if;
            end Print;
            if Ended = 1 then
                exit;
            end if;
        end loop;
    end Printer;

    task type NodeLogic (N : NodePointer; IsLast : Integer) is
        entry Receive (got : PacketPointer);
        entry SetTrap;
    end NodeLogic;

    type Ptr_Logic is access NodeLogic;
    type LogicArray is array (Natural range <>) of Ptr_Logic;
    GraphTasks : LogicArray ( 0 .. NumNodes);
    type PacketArray is array (Natural range <>) of aliased Packet;
    EndPack : PacketArray(0 .. NumPackets-1);
    
    task body NodeLogic is
        CurPack : PacketPointer;
        ExIdx : Integer;
        Ended : Integer;
        GotPack : Integer;
        SendComplete : Integer;
    begin
        Ended := 0;
        if IsLast = 0 then
            loop
                GotPack := 0;
                select
                    accept Receive (got : PacketPointer) do
                        if got.Num = -1 then
                            Ended := 1;
                        else
                            Printer.Print("Pakiet " & Itoa(got.Num) & " jest w wierzchołku " & Itoa(N.Id));
                        end if;
                        CurPack := got;
                        GotPack := 1;
                    end Receive;
                    or
                    accept SetTrap do
                        N.Traps := N.Traps + 1;
                    end SetTrap;
                end select;
                if GotPack = 1 then
                    if Ended = 1 then
                        GraphTasks(N.Exits(0)).Receive(CurPack);
                        exit;
                    end if;
                    CurPack.Path.Append(N.id);
                    N.handled.Append(CurPack.Num);
                    if N.Traps > 0 then
                        N.Traps := N.Traps - 1;
                        Printer.Print("Pakiet " & Itoa(CurPack.Num) & " wpadł w pułapke w wierzchołku " & Itoa(N.Id));
                        CurPack.Dead := 1;
                        Dcnt.Count;
                    else
                        CurPack.Ttl := CurPack.Ttl - 1;
                        if CurPack.Ttl > 0 then
                            RandomDelay;
                            SendComplete := 0;
                            while SendComplete /= 1 loop
                                ExIdx := RandomIdx(Integer(N.Exits.Length));
                                select
                                    GraphTasks(N.Exits(ExIdx)).Receive(CurPack);
                                    SendComplete := 1;
                                or
                                    delay Duration(1);
                                end select;
                            end loop;
                        else
                            Printer.Print("Pakiet " & Itoa(CurPack.Num) & " umarł w wierzchołku " & Itoa(N.Id));
                            CurPack.Dead := 1;
                            Dcnt.Count;
                        end if;
                    end if;
                end if;
            end loop;
        else
            while Ended = 0 loop
                accept Receive (got : PacketPointer) do
                    if got.Num = -1 then
                        Ended := 1;
                    else
                        Printer.Print("Pakiet " & Itoa(got.Num) & " został odebrany");
                        got.Dead := 1;
                        Dcnt.Count;
                    end if;
                end Receive;
            end loop;
        end if;
    end NodeLogic;

    task type hunter is
        entry EndHunt;
    end hunter;
    task body hunter is
        ChosenIdx : Integer;
        Ended : Integer;
    begin
        Ended := 0;
        loop
            ChosenIdx := RandomIdx(NumNodes);
            select
                accept EndHunt do
                    Ended := 1;
                end EndHunt;
            or
                delay Duration(5);
            end select;
            if Ended = 1 then
                exit;
            end if;
            GraphTasks(ChosenIdx).SetTrap;
        end loop;
    end hunter;
    type Ptr_Hunt is access hunter;
    HunterThr : Ptr_Hunt;




    TempInt : Integer;
    TempPack: aliased Packet;
    scMax : Integer;
    scAdded : Integer;
    scIdx : Integer;
    scTarget : Integer;
    scDone : Integer;
    scNIdx : Integer_Vectors.Extended_Index;
    bjMax : Integer;
    bjAdded : Integer;
    bjIdx : Integer;
    bjTarget : Integer;
    bjDone : Integer;
    bjNIdx : Integer_Vectors.Extended_Index;
    


    task body main is
    begin
        Dcnt := new DeadCounter(NumPackets);
        Rand_Int.reset(RandomGen);
        Ada.Numerics.Float_Random.reset(FloatGen);

        for I in Integer range 0 .. NumNodes-1 loop
            Graph(I).Id := I;
            Graph(I).Exits.Append(I+1);
        end loop;

        scMax := ((NumNodes-1)*(NumNodes-2))/2;
        if NumShortcuts > scMax then
            Put_Line("Za dużo skrótów. Ograniczam...");
            NumShortcuts := scMax;
        end if;
        scAdded := 0;

        while scAdded < NumShortcuts loop
            scIdx := -1;
            scTarget := RandomIdx(scMax-scAdded);
            scDone := 0;
            for scStart in Integer range 0 .. NumNodes-2 loop
                for scEnd in Integer range scStart+1 .. NumNodes-1 loop
                    scNIdx := Graph(scStart).Exits.Find_Index(scEnd);
                    if scNidx = Integer_Vectors.No_Index then
                        scIdx := scIdx+1;
                    end if;
                    if scIdx = scTarget then
                        Graph(scStart).Exits.Append(scEnd);
                        scDone := 1;
                        scAdded := scAdded+1;
                        exit;
                    end if;
                end loop;
                if scDone = 1 then
                    exit;
                end if;
            end loop;
        end loop;


        bjMax := ((NumNodes)*(NumNodes-1))/2;
        if NumBackPaths > bjMax then
            Put_Line("Za dużo ścieżek powrotnych. Ograniczam...");
            NumBackPaths := bjMax;
        end if;
        bjAdded := 0;

        while bjAdded < NumBackPaths loop
            bjIdx := -1;
            bjTarget := RandomIdx(bjMax-bjAdded);
            bjDone := 0;
            for bjEnd in Integer range 0 .. NumNodes-2 loop
                for bjStart in Integer range bjEnd+1 .. NumNodes-1 loop
                    bjNIdx := Graph(bjStart).Exits.Find_Index(bjEnd);
                    if bjNidx = Integer_Vectors.No_Index then
                        bjIdx := bjIdx+1;
                    end if;
                    if bjIdx = bjTarget then
                        Graph(bjStart).Exits.Append(bjEnd);
                        bjDone := 1;
                        bjAdded := bjAdded+1;
                        exit;
                    end if;
                end loop;
                if bjDone = 1 then
                    exit;
                end if;
            end loop;
        end loop;

        

        for I in Integer range 0 .. NumNodes-1 loop
            GraphTasks(I) := new NodeLogic(Graph(I)'Access, 0);
        end loop;
        GraphTasks(NumNodes) := new NodeLogic(null, 1);

        for I in Integer range 0 .. NumNodes-2 loop
            Put(Itoa(I) & "->");
            TempInt := Integer(Graph(I).Exits.Length);
            for J in Integer range 0 .. TempInt-1 loop
                Put(Itoa(Graph(I).Exits(J)) & ",");
            end loop;
            Put(" ");
        end loop;
        Put_Line("");

        HunterThr := new hunter;

        for I in Integer range 0 .. NumPackets-1 loop
            EndPack(I).Num := I;
            EndPack(I).Ttl := NumMaxHops;
            EndPack(I).Dead := 0;
            RandomDelay;
            GraphTasks(0).Receive(EndPack(I)'Access);
        end loop;

        
        accept Wat;
        HunterThr.EndHunt;
        TempPack.Num := -1;
        GraphTasks(0).Receive(TempPack'Access);

        Printer.Print("");


        for I in Integer range 0 .. NumNodes-1 loop
            Put("Wierzchołek " & Itoa(i) & " :");
            TempInt := Integer(Graph(I).Handled.Length);
            for J in Integer range 0 .. TempInt-1 loop
                Put(" " & Itoa(Graph(I).Handled(J)));
            end loop;
            Put_Line("");
        end loop;

        for I in Integer range 0 .. NumPackets-1 loop
            Put("Pakiet " & Itoa(EndPack(I).Num) & " :");
            TempInt := Integer(EndPack(I).Path.Length);
            for J in Integer range 0 .. TempInt-1 loop
                Put(" " & Itoa(EndPack(I).Path(J)));
            end loop;
            Put_Line("");
        end loop;
    end main;
        
    
begin
    Prog := new main;
end z1;
