with Ada.Text_IO; use Ada.Text_IO;
with Ada.Containers.Vectors;
with Ada.Strings.Fixed;
with Ada.Numerics.Discrete_Random;
with Ada.Numerics.Float_Random;

procedure z1 is
    NumNodes : constant Integer := 10;
    NumShortcuts : constant Integer := 5;
    NumPackets : constant Integer := 6;
    RandomMillisLimit : constant Integer := 1000;
    
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
    end record;
    type Node is record
        Id : Integer;
        Exits : Integer_Vectors.Vector;
        Handled : Integer_Vectors.Vector;
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
        entry Receive (got : Packet);
        entry EndSync;
    end NodeLogic;

    type Ptr_Logic is access NodeLogic;
    type LogicArray is array (Natural range <>) of Ptr_Logic;
    GraphTasks : LogicArray ( 0 .. NumNodes);
    type PacketArray is array (Natural range <>) of Packet;
    EndPack : PacketArray(0 .. NumPackets-1);
    
    task body NodeLogic is
        CurPack : Packet;
        ExIdx : Integer;
        RcvIdx : Integer;
        Ended : Integer;
    begin
        Ended := 0;
        if IsLast = 0 then
            loop
                accept Receive (got : Packet) do
                    if got.Num = -1 then
                        Ended := 1;
                    else
                        Printer.Print("Pakiet " & Itoa(got.Num) & " jest w wierzchołku " & Itoa(N.Id));
                    end if;
                    CurPack := got;
                end Receive;
                if Ended = 1 then
                    GraphTasks(N.Exits(0)).Receive(CurPack);
                    exit;
                end if;
                CurPack.Path.Append(N.id);
                N.handled.Append(CurPack.Num);
                RandomDelay;
                ExIdx := RandomIdx(Integer(N.Exits.Length));
                GraphTasks(N.Exits(ExIdx)).Receive(CurPack);
            end loop;
        else
            RcvIdx := 0;
            while RcvIdx < NumPackets loop
                accept Receive (got : Packet) do
                    Printer.Print("Pakiet " & Itoa(got.Num) & " został odebrany");
                    EndPack(RcvIdx) := got;
                end Receive;
                RcvIdx := RcvIdx + 1;
            end loop;
            accept EndSync;
        end if;
    end NodeLogic;

    ScStart : Integer;
    ScEnd : Integer;
    TempInt : Integer;
    TempPack: Packet;

begin
    Rand_Int.reset(RandomGen);
    Ada.Numerics.Float_Random.reset(FloatGen);

    for I in Integer range 0 .. NumNodes-1 loop
        Graph(I).Id := I;
        Graph(I).Exits.Append(I+1);
    end loop;

    for I in Integer range 0 .. NumShortcuts-1 loop
        ScStart := RandomIdx(NumNodes);
        ScEnd := ScStart;
        while ScEnd = ScStart loop
            ScEnd := RandomIdx(NumNodes);
        end loop;
        if ScEnd < ScStart then
            TempInt := ScStart;
            ScStart := ScEnd;
            ScEnd := TempInt;
        end if;
        Graph(ScStart).Exits.Append(ScEnd);
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

    for I in Integer range 0 .. NumPackets-1 loop
        TempPack.Num := I;
        RandomDelay;
        GraphTasks(0).Receive(TempPack);
    end loop;

    GraphTasks(NumNodes).EndSync;
    TempPack.Num := -1;
    GraphTasks(0).Receive(TempPack);

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
end z1;
