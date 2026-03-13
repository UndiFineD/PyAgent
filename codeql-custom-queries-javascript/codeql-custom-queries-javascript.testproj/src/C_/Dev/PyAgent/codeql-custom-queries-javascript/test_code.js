// sample JS file for CodeQL pack tests
// we want to catch use of eval and document.write

function badEval(input) {
  return eval(input);
}

function writeDoc(text) {
  document.write(text);
}