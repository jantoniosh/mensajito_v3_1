// mensajito.mx
// Idea Original : Diego Aguirre
// Código: Antonio Salinas

// , String IP, int port 

void receive( byte[] data) {  // <-- extended handler
  String message = new String( data );
  String[] list = split(message, "@");
  String pet = list[0];
  String dato = list[1];
  if(pet.equals("nom")) {
    nombre = dato;
  }
  else if(pet.equals("ubi")) {
    ubicacion = dato;
  }
  else if(pet.equals("mou")) {
    mountPoint = dato;
  }
  else if(pet.equals("ip")) {
    ip = dato;
  }
  else if(pet.equals("int")) {
    internet = dato;
  }
  else if(pet.equals("aud")) {
    audio = dato;
  }
  else if(pet.equals("err")) {
    if (layer == 1) {
      boton_1.change_label("transmitir");
      layer = 0;
    }
  }
  else if(pet.equals("lis")) {
    escuchas = dato;
  }
  else if(pet.equals("mem")) {
    memoria = dato;
  }
}
