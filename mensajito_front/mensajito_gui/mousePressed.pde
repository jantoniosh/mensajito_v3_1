// mensajito.mx
// Idea Original : Diego Aguirre
// Código: Antonio Salinas

void mousePressed() { 
  if (boton_1.MouseIsOver()) {
    if (layer == 0) {
      //get_internet();
      //get_audio();
      println("internet: " + internet);
      println("audio: " + audio);
      if (audio.equals("0") || internet.equals("0")) {
        println("error");
        if (audio.equals("0")) {
          layer = 4;
        }
        else {
          layer = 3;
        }
        boton_1.change_label("volver");
      }
      else {
        layer = 1;
        get_nombre();
        get_ubicacion();
        boton_1.change_label("parar");
        udp.send("tr", "127.0.0.1", 6100);
      }
    }
    else if (layer == 1 || layer == 2 || layer == 3 || layer == 4) {
      boton_1.change_label("transmitir");
      if (layer == 1) {
        udp.send("st", "127.0.0.1", 6100);
      }
      layer = 0;
    }
  }
  if (boton_2.MouseIsOver()) {
    layer = 2;
    get_ip();
    get_mountPoint();
    get_memoria();
    boton_1.change_label("volver");
  }
  //println("layer: " + layer);
}
