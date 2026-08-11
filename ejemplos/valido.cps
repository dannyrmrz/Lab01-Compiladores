// Programa de ejemplo sin errores léxicos ni sintácticos.

const PI: integer = 314;

class Animal {
  let nombre: string;

  function constructor(nombre: string) {
    this.nombre = nombre;
  }

  function hablar(): string {
    return this.nombre + " hace ruido.";
  }
}

class Perro : Animal {
  function hablar(): string {
    return this.nombre + " ladra.";
  }
}

function factorial(n: integer): integer {
  if (n <= 1) {
    return 1;
  }
  return n * factorial(n - 1);
}

/* Los arreglos y los comentarios de varias
   líneas también son parte del lenguaje. */
let notas: integer[] = [90, 85, 100];
let perro: Perro = new Perro("Toby");

foreach (nota in notas) {
  if (nota < 60) {
    continue;
  }
  print(nota);
}

let aprobado: boolean = !(factorial(5) > 100 && PI < 400);
print(perro.hablar());
