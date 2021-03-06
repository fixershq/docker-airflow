const argv = require('minimist')(process.argv.slice(2));
const cryptobject = require('cryptobject');

/**
 * Lookup the function for a given command name.
 * @param {string} name - Command name representing a function.
 * @return {function} The function to be run.
 */
function lookupCommandFunc(name) {
  // func = the js function to run
  let func;
  if (name === 'encrypt') {
    func = cryptobject.encrypt;
  } else if (name === 'decrypt') {
    func = cryptobject.decrypt;
  } else {
    process.stdout.write('ERROR: command "' + name + '" not found');
    process.exit(1);
  }
  return func;
}

/**
 * Apply the desired encryption function, JSONifying from stdin and to stdout.
 *
 * For some reason (see [1]), this write to stdout sometimes fails because the
 * stdout stream has randomly closed [2][3] which breaks the upstream return to
 * Python.
 *
 * 1: https://github.com/aries-data/aries-data/blob/797ea69b1172de1feefd95a07dd4b57c54df9fa8/lib/cli/aries-data.js#L15
 * 2: https://github.com/nodejs/node/issues/947
 * 3: https://github.com/nodejs/node-v0.x-archive/issues/3211
 */
function apply() {
  try {
    const func = lookupCommandFunc(argv.command);
    const rv = func(argv.passphrase, JSON.parse(argv.obj));
    process.stdout.write(JSON.stringify(rv));
    // setTimeout(process.exit.bind(process, 0), 5000);
    process.exit(0);
  } catch (e) {
    process.stdout.write('ERROR: "' + e + '"');
    // console.log(JSON.stringify({}));
    // setTimeout(process.exit.bind(process, 1), 5000);
    process.exit(1);
  }
}

apply();
