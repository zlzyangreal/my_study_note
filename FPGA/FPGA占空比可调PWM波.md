# 占空比可调PWM波

以呼吸灯为例
```verilog
`timescale 1ns / 1ps

module text(
    input   clk,
    input   rst_n,
    output  led,
    output  [15:0] period_cnt,
    output  [15:0] pwm_cycle
);

reg [15:0] period_cnt;
reg [15:0] pwm_cycle;
reg inc_flag;

assign led = (period_cnt <= pwm_cycle) ? 1'b1 : 1'b0;
//counter
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        period_cnt <= 16'd0;
    end
    else begin
        if (period_cnt == 16'd1000) begin
            period_cnt <= 16'd0;
        end
        else begin
            period_cnt <= period_cnt + 16'd1;
        end
    end
end
//pwm
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        pwm_cycle <= 16'd0;
        inc_flag <= 1'b0;
    end
    else begin
        if (!inc_flag) begin
            if (period_cnt>16'd999) begin
                pwm_cycle <= pwm_cycle + 16'd25;
            end
            else begin
                pwm_cycle <= pwm_cycle;
            end
            if (pwm_cycle >= 16'd999) begin
                inc_flag <= 1'b1;
            end
        end
        else begin
            if (period_cnt>16'd999) begin
                pwm_cycle <= pwm_cycle - 16'd25;
            end
            else begin
                pwm_cycle <= pwm_cycle;
            end
            if (pwm_cycle <= 16'd0) begin
                inc_flag <= 1'b0;
            end
        end
    end
end

endmodule
```