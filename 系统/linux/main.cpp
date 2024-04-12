#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
 
int main(int argc, char *argv[])
{
    cv::VideoCapture capture;
    capture.open(0);  //打开摄像头，只要一个摄像头，默认是0; 笔记本上有自带的摄像头,再插入usb摄像头应该是1
    if(capture.isOpened())  //打开摄像头
    {
        std::cout<<"video is open";
    }
    cv::Mat frame; //定义一个矩阵接受帧
    cv::namedWindow("camera",1);  //定义显示帧
    int i=0;
    for(;;)
    {
        capture>>frame; //取出一帧
        if (!frame.empty())
        {
            cv::imshow("camera", frame);   //在窗口显示
            i++;
            std::cout<<i<<"\n";
        }
        else
        {
        }
        cv::waitKey(30); 
    }
    return 0;
}