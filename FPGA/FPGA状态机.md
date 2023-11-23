# 状态机
**状态机三步**，以四路并行信号转为串行为例
```verilog
`timescale 1ns / 1ps
module four_to_one(
    input clk,
    input rst_n,
    input [7:0] fir_dout1,
    input [7:0] fir_dout2,
    input [7:0] fir_dout3,
    input [7:0] fir_dout4,

    output reg [7:0] out_dout
    );

parameter waite_state = 1'b0;
parameter work_state = 1'b1;

reg curr_state;
reg next_state;

reg done_flag;
reg workdone_flag;

reg [31:0] waite_dout;
reg [2:0] cnt;
//一步，下一状态转变
always @(posedge clk or negedge rst_n)begin
    if(!rst_n)
        curr_state <= waite_state;
    else
        curr_state <= next_state;
end
//二步，下一状态判定条件
always @(*)begin
    case(curr_state)
        waite_state : begin
            if(done_flag)
                next_state = work_state;
            else
                next_state = waite_state;
        end
        work_state : begin
            if(workdone_flag)
                next_state = waite_state;
            else
                next_state =work_state;
        end
        default :;
    endcase
end
//三步，每一状态操作
always @(posedge clk or negedge rst_n)begin
    if(!rst_n)begin
        done_flag <= 1'b0;
        workdone_flag <= 1'b0;
        out_dout <= 8'd0;
        waite_dout <= 32'd0;
        cnt <= 3'd0;
    end
    else begin
        case(curr_state)
            waite_state : begin
                workdone_flag <= 1'b0;
                waite_dout <= {fir_dout1,fir_dout2,fir_dout3,fir_dout4};
                done_flag <= 1'b1;
            end
            work_state : begin
                done_flag <= 1'b0;
                case(cnt)
                    3'd0: out_dout <= waite_dout[7:0];
                    3'd1: out_dout <= waite_dout[15:8];
                    3'd2: out_dout <= waite_dout[23:16];
                    3'd3: out_dout <= waite_dout[31:24];
                    default : ;
                endcase
                cnt <= cnt +3'd1;
                if (cnt>3'd3) begin
                    cnt <= 3'd0;
                    workdone_flag <= 1'b1;
                end
            end
        endcase
    end
end

endmodule
```