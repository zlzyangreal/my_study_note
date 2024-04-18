# FPGA分频器
```verilog
`timescale 1ns / 1ps

module text(
    input   clk,
    //The input is set to 10ns inversion, so the input frequency is 500M
    input   rst_n,
    output  clk_25m,
    output  clk_12_5m,
    output  clk_6_25m
);

reg clk_25m;
reg clk_12_5m;
reg clk_6_25m;

reg div_4_cnt;
reg [1:0] div_8_cnt;

//Clock 2 division output 25MHz clock
always @(posedge clk or negedge rst_n) begin
    if(!rst_n)
        clk_25m <= 1'b0;
    else 
        clk_25m <= ~clk_25m;
end

//Clock 4 division output 12.5MHz clock
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        clk_12_5m <= 1'b0;
        div_4_cnt <= 1'b0;
    end  
    else begin
        div_4_cnt <= div_4_cnt + 1'b1;
        if(div_4_cnt == 1'b1)
//Adding 1 all the way causes a two-bit overflow, so you have a loop of 0s and 1s
            clk_12_5m <= ~clk_12_5m;
    end        
end
//Clock 8 division output 6.25MHz clock
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        clk_6_25m <= 1'b0;
        div_8_cnt <= 2'b00;
    end
    else begin
        div_8_cnt <= div_8_cnt + 1'b1;
        if(div_8_cnt == 2'b11)
            clk_6_25m <= ~clk_6_25m;
    end
end

endmodule
```