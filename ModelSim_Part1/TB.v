module A;
    reg [7:0] A;
    reg [7:0] B;
    wire [15:0] P;
    part1 U( A, B, P );

    initial begin
        $dumpfile ("testII.vcd");
        $dumpvars (0,A);
    
    end
endmodule
