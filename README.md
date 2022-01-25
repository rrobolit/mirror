# mirror

[Mirror stand - minor software modifications](https://drive.google.com/drive/folders/1j5hN2-Xuf_q-nPx8kCNg1D-OUZJdoBgo?usp=sharing "Google Drive") - project work: minor modifications to several software modules of exhibition stand - matrix of moving mirrors which try to reflect shape of person. Human identification was done by 2 cameras + openCv in Unity 3D (Intel Nuc). Mech part - A LOT of RC servos and Arduino. Stack: Unity 3D; Python 3.x; Arduino, FlProg

#### My part:
- **change data transfer from Unity yo Arduino**: was serial, need to be ModbusTCP. Was done via intermediate python script: socket server for incoming data from Unity + 3 processes with ModbusTCP clients for Arduino. Python makes all data transformation
- **debug programs for mirrors motors check**: was done by several python scripts
- **increase speed of data transfer via I2C in arduino**: unreasonably low data transfer speed resulting in 'wave' effect. Was done by searching and correcting problem part in Arduino I2C library.
