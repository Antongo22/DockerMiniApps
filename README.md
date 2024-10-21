# DockerMiniApps

To get started, make sure that you have docker and docker-compose installed.

Write: 
<pre><code id="clone-command" class="language-bash">git clone https://github.com/Antongo22/DockerMiniApps.git</code></pre>
<button onclick="copyToClipboard('clone-command')">Copy</button>

Open the "DockerMiniApps" directory and write: 
<pre><code id="build-command" class="language-bash">docker-compose up --build</code></pre>
<button onclick="copyToClipboard('build-command')">Copy</button>

Then go to <a href="http://localhost:8002/">http://localhost:8002/</a>

<script>
function copyToClipboard(elementId) {
  var text = document.getElementById(elementId).innerText;
  var textArea = document.createElement("textarea");
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand("Copy");
  textArea.remove();
  alert("Copied to clipboard: " + text);
}
</script>
