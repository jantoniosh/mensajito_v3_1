// mensajito.mx
// Idea Original : Diego Aguirre
// Código: Antonio Salinas

import hypermedia.net.*;

UDP udp;

//Button boton_1, boton_2;
Button boton_1, boton_2;
int clk = 1;
int layer;
boolean trsm;
PFont main_font;
String nombre, ubicacion, escuchas, mountPoint, ip, memoria, internet, audio;
PImage estacion, logo, fondo;

void setup() {
  nombre = "";
  ubicacion = "";
  escuchas = "";
  internet = "";
  audio = "";
  fullScreen();
  layer = 0;
  //size(480,320);
  main_font = createFont("CircularStd-Medium.otf", 28);
  noCursor();
  textFont(main_font);
  smooth();
  textSize(18);
  boton_1 = new Button("transmitir", 10, 220, 140, 60);
  boton_2 = new Button("info", 330, 220, 140, 60);
  trsm = false;
  logo = loadImage("logo.jpg");
  fondo = loadImage("/home/pi/grafica/fondo.jpg");
  udp = new UDP(this, 6000);
  udp.listen(true);
  get_internet();
  get_audio();
}

void draw() {
  if(layer == 0) {
    layer_main();
  }
  else if(layer == 1){
    layer_trns();
  }
  else if(layer == 2){
    layer_info();
  }
  else if(layer == 3){
    layer_internet();
  }
  else if(layer == 4){
    layer_audio();
  }
}

void layer_main() {
  background(fondo);
  textSize(28);
  boton_1.Draw();
  boton_2.Draw();
}

void layer_trns() {
  background(175);
  fill(0);
  textSize(28);
  textAlign(LEFT);
  text(nombre, 10, 60);
  text("transmitiendo desde", 10, 100);
  text(ubicacion, 10, 140);
  text("escuchas: " + escuchas, 10, 180);
  textSize(28);
  boton_1.Draw();
  fill(255, 0, 0);
  noStroke();
  ellipse(260, 253, 20, 20);
  text("en vivo", 200, 250);
  image(logo, 300, 120, 170, 170);
}

void layer_info() {
  background(175);
  fill(0);
  textSize(28);
  textAlign(LEFT);
  text("dirección stream:", 10, 60);
  text("mensajito.mx:8000/" + mountPoint, 10, 100);
  text("IP: " + ip, 10, 140);
  text("memoria: " +  memoria, 10, 180);
  textSize(28);
  boton_1.Draw();
}

void layer_internet() {
  background(175);
  fill(0);
  textSize(28);
  textAlign(LEFT);
  text("sin conexión a internet\n\n:( :( :( :( ", 10, 60);
  textSize(28);
  boton_1.Draw();
}

void layer_audio() {
  background(175);
  fill(0);
  textSize(28);
  textAlign(LEFT);
  text("sin interfaz usb\n\n:( :( :( :( ", 10, 60);
  textSize(28);
  boton_1.Draw();
}
