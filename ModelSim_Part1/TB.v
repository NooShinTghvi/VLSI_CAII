module A;
    reg [7:0] A;
    reg [7:0] B;
    wire [15:0] P;
    part1 U( A, B, P );

    initial begin
        $dumpfile ("testI.vcd");
        $dumpvars;
    
    end
endmodule
