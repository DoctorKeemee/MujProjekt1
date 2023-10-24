<template>
  <div class="word-card" >
    <div class="word" id="word">{{ currentWord }}</div>
    <div class="definition" id="definition">{{ currentDefinition }}</div>
  </div>
  <button @click="showNextWord" style="background: green">Chápu to!</button>

  <button @click="chooseFile" style="background: darkorange">Import from XLSX</button>
  <button @click="exportToCSV" style="background: darkred">Export to XLSX</button>
  <input type="file" ref="fileInput" style="opacity: 0;" @change="importFromCSV" accept=".csv">

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
        ],
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
.word-card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 2px 2px 5px #aaa;
  width: 300px;
  text-align: center;
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