with Ada.Text_IO; use Ada.Text_IO;
with Ada.Containers; use Ada.Containers;
with Ada.Containers.Vectors;
with Ada.Containers.Doubly_Linked_Lists;
with Ada.Strings.Fixed;
with Ada.Strings.Unbounded;
with Ada.Numerics.Float_Random;
with Ada.Command_Line; use Ada.Command_Line;
with Ada.Characters;
with Ada.Characters.Latin_1;

procedure z1 is
    Ending : Boolean := False;

    protected type DeadCounterType is
        procedure Increment (By : Integer);
        entry Wait;
    private
        Value : Integer := 0;
        IsReady : Boolean := False;
        Triggered : Integer := 0;
    end DeadCounterType;
    protected body DeadCounterType is
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
    end DeadCounterType;
    DeadCounter : DeadCounterType;
    HostsDeadCounter : DeadCounterType;

    package Integer_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => Integer);

    type Packet is record
        FromRouter : Integer;
        FromHost : Integer;
        ToRouter : Integer;
        ToHost : Integer;
        Path : Integer_Vectors.Vector;
    end record;

    package Packet_Lists is new Ada.Containers.Doubly_Linked_Lists (Element_Type => Packet);
    
    protected type SQueue is
        procedure Push (Data : Packet);
        entry Get (Data : out Packet);
    private
        Store : Packet_Lists.List;
        NotEmpty : Boolean := False;
    end SQueue;
    protected body SQueue is
        procedure Push (Data : Packet) is
        begin
            Store.Append(Data);
            NotEmpty := True;
        end Push;
        entry Get (Data : out Packet) when NotEmpty is
        begin
            Data := Store.First_Element;
            Store.Delete_First;
            if Integer(Store.Length) = 0 then
                NotEmpty := False;
            end if;
        end Get;
    end Squeue;
    
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
    
    package Routing_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => RoutingEntry);

    protected type RoutingTable is
        procedure GetData (D : out Routing_Vectors.Vector);
        procedure PushData (V : Routing_Vectors.Vector);
        function CheckData return Boolean;
        procedure AppendData (E : RoutingEntry);
        procedure SetParent (I : Integer);
        procedure DumpData (D : out Routing_Vectors.Vector);
        procedure GetPath (T : Integer; D : out Integer);
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

        procedure GetPath (T : Integer; D : out Integer) is
        begin
            D := Table(T).NextHop;
        end GetPath;
    end RoutingTable;
        
    
    
    type Node is record
        Id : Integer;
        Exits : Integer_Vectors.Vector;
        Table : RoutingTable;
        Hosts : Integer_Vectors.Vector;
        Queue : SQueue;
        HostsNum : Integer;
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
                delay (Duration(RandomIdx(10000)) / 1000.0);
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
                        --Printer.Print(Ada.Strings.Unbounded.To_String(TempStr));
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

    task type ForwarderReceiver (N : NodePointer) is
        entry Receive (got : Packet);
        entry Kill;
    end ForwarderReceiver;

    task type ForwarderSender (N : NodePointer) is
    end ForwarderSender;
    
    task type HostLogic(N : NodePointer; HostID : Integer) is
        entry Receive (got : Packet);
        entry Start;
        entry Kill;
    end HostLogic;
    
    type HostLogicPointer is access HostLogic;
    package Host_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => HostLogicPointer);
    HostsStore : Host_Vectors.Vector;

    type ForwarderReceiverPointer is access ForwarderReceiver;
    package Forwarder_Receiver_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => ForwarderReceiverPointer);
    Forwarder_Receivers : Forwarder_Receiver_Vectors.Vector;

    type ForwarderSenderPointer is access ForwarderSender;
    package Forwarder_Sender_Vectors is new Ada.Containers.Vectors (Index_Type => Natural, Element_Type => ForwarderSenderPointer);
    Forwarder_Senders : Forwarder_Sender_Vectors.Vector;

    task body ForwarderReceiver is
        EndPack : Packet;
        Ended : Boolean := False;
    begin
        EndPack.ToRouter := -1;
        loop
            select
                accept Receive (got : Packet) do
                    N.Queue.Push(got);
                end Receive;
            or
                accept Kill do
                    N.Queue.Push(EndPack);
                    Ended := True;
                end Kill;
            end select;
            if Ended = True then
                exit;
            end if;
        end loop;
    end ForwarderReceiver;

    task body ForwarderSender is
        Processed : Packet;
        Next : Integer;
    begin
        loop
            N.Queue.Get(Processed);
            if Processed.ToRouter = -1 then
                exit;
            end if;
            Processed.Path.Append(N.Id);
            if Processed.ToRouter = N.Id then
                HostsStore(N.Hosts(Processed.ToHost)).Receive(Processed);
            else
                N.Table.GetPath(Processed.ToRouter, Next);
                Forwarder_Receivers(Next).Receive(Processed);
            end if;
        end loop;
    end ForwarderSender;

    
    task body HostLogic is
        MyPacket : Packet;
        TempStr : Ada.Strings.Unbounded.Unbounded_String;
        Ended : Boolean := False;
    begin
        accept Start;
        MyPacket.FromRouter := N.Id;
        MyPacket.FromHost := HostID;
        MyPacket.ToRouter := RandomIdx(Integer(Graph.Length));
        MyPacket.ToHost := RandomIdx(Integer(Graph(MyPacket.ToRouter).Hosts.Length));
        --Printer.Print("Wysylam pakiet od (" & Itoa(MyPacket.FromRouter) & "," & Itoa(MyPacket.FromHost) & ") do (" & Itoa(MyPacket.ToRouter) & "," & Itoa(MyPacket.ToHost) & ")");
        Forwarder_Receivers(N.Id).Receive(MyPacket);
        loop
            select
                accept Receive (got : Packet) do
                    MyPacket := got;
                end Receive;
            or
                accept Kill do
                    Ended := True;
                end Kill;
            end select;

            if Ended = True then
                exit;
            end if;
                
            TempStr := Ada.Strings.Unbounded.To_Unbounded_String("");
            Ada.Strings.Unbounded.Append(TempStr,"pakiet od (" & Itoa(MyPacket.FromRouter) & "," & Itoa(MyPacket.FromHost) & ") doszedl do (" & Itoa(MyPacket.ToRouter) & "," & Itoa(MyPacket.ToHost) & ") trasa: ");
            for L of MyPacket.Path loop
                Ada.Strings.Unbounded.Append(TempStr, Itoa(L) & ",");
            end loop;
            Printer.Print(Ada.Strings.Unbounded.To_String(TempStr));

            if Ending = True then
                HostsDeadCounter.Increment(-1);
            else
                MyPacket.ToRouter := MyPacket.FromRouter;
                MyPacket.ToHost := MyPacket.FromHost;
                MyPacket.FromRouter := N.Id;
                MyPacket.FromHost := HostID;
                MyPacket.Path.Clear;
                delay (Duration(RandomIdx(1000)) / 1000.0);
                Forwarder_Receivers(N.Id).Receive(MyPacket);
            end if;
        end loop;
    end HostLogic;

        

    
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

    NewHost : HostLogicPointer;
    NumHosts : Integer;
    
        
    
begin
    NumNodes := Integer'Value(Argument(1));
    NumShortcuts := Integer'Value(Argument(2));

    Ada.Numerics.Float_Random.reset(FloatGen);

    for I in Integer range 0 .. NumNodes-1 loop
        NewNode := new Node;
        NewNode.Id := I;
        NewNode.HostsNum := RandomIdx(2) + 1;
        Graph.Append(NewNode);
        Graph(I).Table.SetParent(I);
        for J in Integer range 0 .. Graph(I).HostsNum-1 loop
            NewHost := new HostLogic(Graph(I), J);
            Graph(I).Hosts.Append(Integer(HostsStore.Length));
            HostsStore.Append(NewHost);
        end loop;
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
        Put("(router: " & Itoa(I) & " hosty: " & Itoa(Graph(I).HostsNum) & " )->");
        TempInt := Integer(Graph(I).Exits.Length);
        for J in Integer range 0 .. TempInt-1 loop
            Put(Itoa(Graph(I).Exits(J)) & ",");
        end loop;
        Put(" ");
    end loop;
    Put_Line("");


    DeadCounter.Increment(NumNodes);
    HostsDeadCounter.Increment(Integer(HostsStore.Length));

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
        Forwarder_Receivers.Append(new ForwarderReceiver(Graph(I)));
        Forwarder_Senders.Append(new ForwarderSender(Graph(I)));
    end loop;

    for I in Integer range 0 .. NumNodes-1 loop
        Mail.Append(new Sender(Graph(I)));
        for J in Integer range 0 .. Graph(I).HostsNum-1 loop
            HostsStore(Graph(I).Hosts(J)).Start;
        end loop;
    end loop; 

    DeadCounter.Wait;
    --Put_Line("Koniec zmian w routingu");
    Ending := True;
    HostsDeadCounter.Wait;
    --Put_Line("Wszystkie pakiety zjedzone");
    
    for I in Integer range 0 .. NumNodes-1 loop
        Mail(I).Kill;
        Forwarder_Receivers(I).Kill;
    end loop;

    NumHosts := Integer(HostsStore.Length);
    for I in Integer range 0 .. NumHosts-1 loop
        HostsStore(I).Kill;
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
