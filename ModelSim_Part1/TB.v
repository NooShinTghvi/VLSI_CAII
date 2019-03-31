module A;
    reg [7:0] A;
    reg [7:0] B;
    wire [15:0] P;
    part1 U( A, B, P );
    initial begin
        $dumpfile ("test3.vcd");
        A   = 8'b01010101;
        B   = 8'b10101010;
        //#200
        $dumpvars(0);
        //$stop();
    end
	//always #10 A = A + 1;
    //always #20 B = B + 1;
	//initial begin
		
	//	
	//end
endmodule
