
`timescale 1ns / 1ps
module part1_tb();
reg [15:0] in_ram [0:49999];
reg [7:0] A;
reg [7:0] B;
wire [15:0] P;
integer x;
part1 U( A, B, P );

initial begin
  $readmemb("input.txt", in_ram);
  $dumpfile ("myFinalTest.vcd");
  $dumpvars(0, part1_tb);
  for(x = 0; x < 50000; x = x + 1) begin
    #53
    $display("%d",x);
    A = in_ram[x][15 : 8];
    B = in_ram[x][7 : 0];
  end
end

      
endmodule
