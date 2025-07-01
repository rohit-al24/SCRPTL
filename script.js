// 🔤 Tunglish → Python translator
function tunglishToPython(code) {
  const map = {
    'varunga': '',
    'sollu': 'print',
    'nalla_irundha': 'if',
    'illa_na': 'else',
    'pirichu': 'elif',
    'saar': 'def',
    'mudichachu': 'return',
    'varuven': 'while',
    'paaru': 'input',
    'poitu varen': 'break'
  };

  let lines = code.split('\n');
  let translated = lines.map(line => {
    for (const [tunglish, python] of Object.entries(map)) {
      const regex = new RegExp(`\\b${tunglish}\\b`, 'g');
      line = line.replace(regex, python);
    }
    return line;
  });

  return translated.join('\n');
}

// ▶️ Execute the translated code (basic eval simulation)
async function runCode() {
  const tunglishCode = document.getElementById('editor').value;
  const pythonCode = tunglishToPython(tunglishCode);
  document.getElementById('translatedCode').innerText = pythonCode;

  try {
    const response = await fetch('http://127.0.0.1:5000/run', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ code: pythonCode })
    });

    const result = await response.json();
    const { output, errors } = result;

    document.getElementById('outputBox').innerText =
      output || errors || '(No output)';
  } catch (err) {
    document.getElementById('outputBox').innerText =
      '❌ Error connecting to backend:\n' + err.message;
  }
}


// 🔍 Show the keyword modal
function showHelp() {
  document.getElementById('popup').classList.remove('hidden');
}

// ❌ Close the modal
function hideHelp() {
  document.getElementById('popup').classList.add('hidden');
}
