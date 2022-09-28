with Ada.Text_IO; use Ada.Text_IO;
with Ada.Containers; use Ada.Containers;
with Ada.Containers.Vectors;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded;
with Ada.Numerics.Float_Random;
with Ada.Command_Line; use Ada.Command_Line;
with Ada.Characters;
with Ada.Characters.Latin_1;

procedure z1 is

    protected DeadCounter is
        procedure Increment (By : Integer);
        entry Wait;
    private
        Value : Integer := 0;
        IsReady : Boolean := False;
        Triggered : Integer := 0;
    end DeadCounter;
    protected body DeadCounter is
        procedure Increment (By : Integer) is
        begin
            Value := Value + By;
            if Value <= 0 then
                IsReady := True;
            end if;
        end Increment;
        entry Wait when IsReady is
        begin
            Triggered := Triggered+1;
        end Wait;
    end DeadCounter;
    
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

    protected Printer is
        procedure Print (line : String);
    end Printer;
    protected body Printer is
        procedure Print (line : String) is
        begin
            Put_Line(line);
        end Print;
    end Printer;

    type RoutingEntry is record
        Dest : Integer;
        Cost : Integer;
        NextHop : Integer;
        Changed : Boolean;
    end record;
    
    
    package Integer_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => Integer);
    package Routing_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => RoutingEntry);

    protected type RoutingTable is
        procedure GetData (D : out Routing_Vectors.Vector);
        procedure PushData (V : Routing_Vectors.Vector);
        function CheckData return Boolean;
        procedure AppendData (E : RoutingEntry);
        procedure SetParent (I : Integer);
        procedure DumpData (D : out Routing_Vectors.Vector);
    private
        Table : Routing_Vectors.Vector;
        Newdata : Boolean := True;
        MyNode : Integer := -1;
    end RoutingTable;
    protected body RoutingTable is
        procedure GetData (D : out Routing_Vectors.Vector) is
        begin
            for E of Table loop
                if E.Changed then
                    E.Changed := False;
                    D.Append(E);
                end if;
            end loop;
            if D.Length > 0 then
                DeadCounter.Increment(-1);
            end if;
            Newdata := False;
        end GetData;

        procedure PushData (V : Routing_Vectors.Vector) is
        begin
            for E of V loop
                if E.Cost < Table(E.Dest).Cost then
                    Printer.Print("Zmiana: wierzcholek " & Itoa(MyNode) & " trasa do " & Itoa(E.Dest) & " przez " & Itoa(E.NextHop) & " koszt " & Itoa(E.Cost));
                    Table(E.Dest).Cost := E.Cost;
                    Table(E.Dest).NextHop := E.NextHop;
                    Table(E.Dest).Changed := True;
                    if Newdata = False then
                        DeadCounter.Increment(1);
                        Newdata := True;
                    end if;
                end if;
            end loop;
        end PushData;

        function CheckData return Boolean is
        begin
            return Newdata;
        end CheckData;

        procedure AppendData (E : RoutingEntry) is
        begin
            Table.Append(E);
        end AppendData;

        procedure SetParent (I : Integer) is
        begin
            MyNode := I;
        end SetParent;

        procedure DumpData (D : out Routing_Vectors.Vector) is
        begin
            D := Table;
        end DumpData;
    end RoutingTable;
        
        
    
    type Node is record
        Id : Integer;
        Exits : Integer_Vectors.Vector;
        Table : RoutingTable;
    end record;
    
    type NodePointer is access all Node;
    package Node_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => NodePointer);
    Graph : Node_Vectors.Vector;


    task type Receiver (N : NodePointer) is
        entry Receive (got : Routing_Vectors.Vector);
        entry Kill;
    end Receiver;
    task body Receiver is
        Data : Routing_Vectors.Vector;
        Killed : Boolean := False;
    begin
        loop
            select
                accept Receive (got : Routing_Vectors.Vector) do
                    Data := got;
                    DeadCounter.Increment(1);
                end Receive;
            or
                accept Kill do
                    Killed := True;
                end Kill;
            end select;
            if Killed then
                exit;
            end if;
            for E of Data loop
                E.Cost := E.Cost+1;
            end loop;
            N.Table.PushData(Data);
            DeadCounter.Increment(-1);
        end loop;
    end Receiver;

    type ReceiverPointer is access Receiver;
    package Receiver_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => ReceiverPointer);
    Comms : Receiver_Vectors.Vector;

    task type Sender (N : NodePointer) is
        entry Kill;
    end Sender;
    task body Sender is
        Data : Routing_Vectors.Vector;
        Killed : Boolean := False;
        TempStr : Ada.Strings.Unbounded.Unbounded_String;
    begin
        loop
            select
                accept Kill do
                    Killed := True;
                end Kill;
            or
                delay (Duration(RandomIdx(5000)) / 1000.0);
            end select;
            if Killed then
                exit;
            end if;
            if N.Table.CheckData then
                DeadCounter.Increment(1);
                Routing_Vectors.Clear(Data);
                N.Table.GetData(Data);
                for E of Data loop
                    E.NextHop := N.Id;
                end loop;
                if Routing_Vectors.Length(Data) > 0 then
                    for Neigh of N.Exits loop
                        TempStr := Ada.Strings.Unbounded.To_Unbounded_String("");
                        Ada.Strings.Unbounded.Append(TempStr,"Oferta: z wierzchołka " & Itoa(N.Id) & " do " & Itoa(Neigh) & " : ");
                        for L of Data loop
                            Ada.Strings.Unbounded.Append(TempStr,Ada.Characters.Latin_1.LF & "   dest: " & Itoa(L.Dest)  & " nexthop: " & Itoa(L.NextHop) & " cost: " & Itoa(L.Cost+1));
                        end loop;
                        Printer.Print(Ada.Strings.Unbounded.To_String(TempStr));
                        Comms(Neigh).Receive(Data);
                    end loop;
                end if;
                DeadCounter.Increment(-1);
            end if;
        end loop;
    end Sender;

    type SenderPointer is access Sender;
    package Sender_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => SenderPointer);
    Mail : Sender_Vectors.Vector;

    NumNodes : Integer;
    NumShortcuts : Integer;
    TempInt : Integer;
    scMax : Integer;
    scAdded : Integer;
    scIdx : Integer;
    scTarget : Integer;
    scDone : Integer;
    scNIdx : Integer_Vectors.Extended_Index;

    NewNode : NodePointer;
    TempRoute : RoutingEntry;
    TempRtab : Routing_Vectors.Vector;
    
        
    
begin
    NumNodes := Integer'Value(Argument(1));
    NumShortcuts := Integer'Value(Argument(2));

    Ada.Numerics.Float_Random.reset(FloatGen);

    for I in Integer range 0 .. NumNodes-1 loop
        NewNode := new Node;
        NewNode.Id := I;
        Graph.Append(NewNode);
        Graph(I).Table.SetParent(I);
    end loop;

    for I in Integer range 0 .. NumNodes-2 loop
        Graph(I).Exits.Append(I+1);
        Graph(I+1).Exits.Append(I);
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
                    Graph(scEnd).Exits.Append(scStart);
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


    for I in Integer range 0 .. NumNodes-1 loop
        Put(Itoa(I) & "->");
        TempInt := Integer(Graph(I).Exits.Length);
        for J in Integer range 0 .. TempInt-1 loop
            Put(Itoa(Graph(I).Exits(J)) & ",");
        end loop;
        Put(" ");
    end loop;
    Put_Line("");


    DeadCounter.Increment(NumNodes);

    for I in Integer range 0 .. NumNodes-1 loop
        for J in Integer range 0 .. NumNodes-1 loop
            TempRoute.Dest := J;
            TempRoute.Changed := True;
            if I = J then
                TempRoute.Cost := 0;
                TempRoute.NextHop := I;
                TempRoute.Changed := False;
            else
                scNidx := Graph(I).Exits.Find_Index(J);
                if scNidx = Integer_Vectors.No_Index then
                    if J < I then
                        TempRoute.NextHop := I-1;
                        TempRoute.Cost := I-J;
                    else
                        TempRoute.NextHop := I+1;
                        TempRoute.Cost := J-I;
                    end if;
                else
                    TempRoute.Cost := 1;
                    TempRoute.NextHop := J;
                end if;
            end if;
            Graph(I).Table.AppendData(TempRoute);
        end loop;
    end loop;
    

    for I in Integer range 0 .. NumNodes-1 loop
        Comms.Append(new Receiver(Graph(I)));
    end loop;

    for I in Integer range 0 .. NumNodes-1 loop
        Mail.Append(new Sender(Graph(I)));
    end loop; 

    DeadCounter.Wait;
    
    for I in Integer range 0 .. NumNodes-1 loop
        Mail(I).Kill;
    end loop;

    for I in Integer range 0 .. NumNodes-1 loop
        Comms(I).Kill;
    end loop;

    for I in Integer range 0 .. NumNodes-1 loop
        Graph(I).Table.DumpData(TempRtab);
        for J in Integer range 0 .. NumNodes-1 loop
            Put_Line("Wierzcholek " & Itoa(I) & " trasa do " & Itoa(J) & " koszt " & Itoa(TempRtab(J).Cost) & " przez " & Itoa(TempRtab(J).NextHop));
        end loop;
    end loop;
end z1;
