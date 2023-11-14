<template>
  <nav class="menu">
    <button @click="chooseFile" class="button darkorange">Import from XLSX</button>
    <button @click="exportToCSV" class="button red_button" > Export to XLSX</button>
  </nav>
  <div class="container" >
    <div class="word-card" >
    <div class="word" id="word">{{ currentWord }}</div>
    <div class="definition" id="definition">{{ currentDefinition }}</div>
  </div>
  <button @click="showNextWord" class="button green_button">Chápu to!</button>
  <input type="file" ref="fileInput" style="opacity: 0;" @change="importFromCSV" accept=".csv">
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from "vue";

  export default defineComponent({
    name: "Learning",
    data() {
      return {
        wordList: [
          { word: "Ubiquitous", definition: "Existing or being everywhere at the same time", explained: false },
          { word: "Sycophant", definition: "A person who acts obsequiously towards someone important", explained: false  },
          { word: "Ephemeral", definition: "Lasting for a very short time", explained: false  }
        ] as { word: string; definition: string; explained: boolean }[],
        currentIndex: ref(0),
      };
    },
    computed: {
      currentWord(){
        return this.wordList[this.currentIndex].word;
      },
      currentDefinition(){
        return this.wordList[this.currentIndex].definition;
      },
    },
    methods: {
      chooseFile() {
        // Trigger the file input element when the button is clicked
        var x = this.$refs?.fileInput as HTMLInputElement | null;
        if(x != null)x.click();
      },
      showNextWord() {
        if (this.currentIndex < this.wordList.length) {
          this.currentIndex++;
        } else {
          //TODO return just new words
          this.currentIndex = 0; // Loop back to the first word
        }
      },
      importFromCSV(event: Event){
        const fileInput = event.target as HTMLInputElement | null;
        if(fileInput==null)return;
        const file = fileInput.files?.[0];

        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            const csvData = (e.target as FileReader).result as string; // Typecast to string
            this.parseCSV(csvData);
          };
          reader.readAsText(file);
        }
      },
      parseCSV(csvData: string) {
        console.log(csvData);
        const lines: string[] = csvData.split('\n');
        this.wordList = [] as { word: string; definition: string; explained: boolean }[]
        for (let i = 0; i < lines.length; i++) {
          const word: string[] = lines[i] .split(';');
          this.wordList.push({
            word: word[0],
            definition: word[1],
            explained: false,
          });
        }

      },
      exportToCSV(){
        //todo make a header
        //export data
        const csvContent = "data:text/csv;charset=utf-8," + this.wordList.map((item) => {
          return `${item.word};${item.definition}`;
        }).join("\n");

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "wordList.csv");
        document.body.appendChild(link); // Required for Firefox
        link.click();
      }
    }
  })
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}
nav{
  margin-top: 15px;
  margin-bottom: 150px;
}
.button{
  color: antiquewhite;
  font-size: larger;
  padding: 5px;
  margin: 5px;
}
.green_button {
  background: green;
}
.red_button{
  background: darkred;
}
.darkorange{
  background: darkorange;
}
.word-card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 2px 2px 5px #aaa;
  width: 300px;
  text-align: center;
  background: #181717;
  background-image: url("https://image.api.playstation.com/vulcan/img/cfn/11307x4B5WLoVoIUtdewG4uJ_YuDRTwBxQy0qP8ylgazLLc01PBxbsFG1pGOWmqhZsxnNkrU3GXbdXIowBAstzlrhtQ4LCI4.png");
  background-repeat: no-repeat;
  background-position: right top;
  color: black;
}
.word {
  font-size: 36px;
  font-weight: bold;
}
.definition {
  margin-top: 10px;
  font-size: 18px;
}
</style>