`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/11/28 10:10:39
// Design Name: 
// Module Name: sim
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module sim();

reg clk;
reg rst_n;
reg [4:0] din;

wire [7:0] dout1;
wire [7:0] dout2;
// wire [4:0] text1;
// wire [4:0] text2;
// wire text_en;

always #10 clk=~clk;

initial begin
    clk = 0;
    rst_n = 0;
    #100 rst_n = 1;
end

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        din <= 0;
    end
    else begin
        din <= din + 1;
        if (din >= 9) begin
            din <= 0;
        end
    end
end

fir6 u_fir6 (
    .clk(clk),
    .rst_n(rst_n),
    .din(din),
    .dout(dout1)
);

flod_fir6_top u_flod_fir6_top (
    .clk(clk),
    .rst_n(rst_n),
    .din(din),
    .dout(dout2)
);


endmodule
