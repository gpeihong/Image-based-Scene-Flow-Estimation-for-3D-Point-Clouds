clc;
clear;
close all;
fid=fopen('./0000000008.bin','rb');
[a,count]=fread(fid,'float32');
fclose(fid);%¹Ø±ÕÎÄ¼þ
x = round(a(1:4:end)*100);
y = round(a(2:4:end)*100);
z = round(a(3:4:end)*100);
intensity= vpa(a(4:4:end)*100);
data = pointCloud(single([x y z ]),'intensity',single(intensity));
pcshow(data);
pcwrite(data,'0000000008.ply','PLYFormat','ascii');
%img=pcread('0000000001.ply');
%pcwrite(img,'0000000001.pcd');