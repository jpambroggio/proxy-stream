const express = require('express');
const request = require('request');
const app = express();

// Cambia este link por el que quieras transmitir
const STREAM_URL = 'http://190.94.160.6:8081/hls/hd-live.m3u8';

app.get('/', (req, res) => {
  res.send('Servidor Proxy funcionando para el Stream.');
});

app.get('/stream.m3u8', (req, res) => {
  request
    .get(STREAM_URL)
    .on('error', function(err) {
      console.error(err);
      res.status(500).send('Error en el Stream');
    })
    .pipe(res);
});

// Escucha en el puerto que Render asigna automáticamente
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en el puerto ${PORT}`);
});