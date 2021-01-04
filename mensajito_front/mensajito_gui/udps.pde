void get_nombre() {
  udp.send("nom", "127.0.0.1", 6100);
}

void get_ubicacion() {
  udp.send("ubi", "127.0.0.1", 6100);
}

void get_mountPoint() {
  udp.send("mou", "127.0.0.1", 6100);
}

void get_ip() {
  udp.send("ip", "127.0.0.1", 6100);
}

void get_internet() {
  udp.send("int", "127.0.0.1", 6100);
}

void get_audio() {
  udp.send("aud", "127.0.0.1", 6100);
}

void get_status() {
  udp.send("sta", "127.0.0.1", 6100);
}

void get_escuchas() {
  udp.send("esc", "127.0.0.1", 6100);
}

void get_memoria() {
  udp.send("mem", "127.0.0.1", 6100);
}
