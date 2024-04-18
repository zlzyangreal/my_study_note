# 循环语句
```verilog
generate
genvar i;
for(i=0;i<64;i=i+1)
	begin
	always@(posedge clk or negedge rst)
		if(!rst)
			dist[i]<=0;
		else 
			dist[i]<=1          
	end
endgenerate
```