<template>
  <nav
      class="navbar is-fixed-top is-warning"
      role="navigation"
      aria-label="main navigation"
  >
    <div class="navbar-brand">
      <a class="navbar-item" href="https://bulma.io">
        <img src="https://bulma.io/images/bulma-logo.png" width="112" height="28">
      </a>

      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div class="navbar-start">
  <RouterLink to="/" class="navbar-item">Domů</RouterLink>
  <RouterLink to="/practicing" class="navbar-item">Procvičování</RouterLink>
  <RouterLink to="/learning" class="navbar-item">Učení</RouterLink>
      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">
          Data management
        </a>

        <div class="navbar-dropdown">
        <a @click="chooseFile" class="navbar-item">Import XLSX</a>
          <input type="file" ref="fileInput" style="opacity: 0;" @change="importFromCSV" accept=".csv">
        <a @click="exportToCSV" class="navbar-item" > Export XLSX</a>
      </div>
    </div>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a class="button is-primary">
            <strong>Sign up</strong>
          </a>
          <a class="button is-light">
            Log in
          </a>
        </div>
      </div>
    </div>

  </nav>
</template>

<script lang="ts">

import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "Navigation",
  data() {
    return {
      wordList: [ ] as { word: string; definition: string; explained: boolean; level: number | null }[],
      currentIndex: ref(0),
    };
  },
  methods: {
    chooseFile() {
      // Trigger the file input element when the button is clicked
      var x = this.$refs?.fileInput as HTMLInputElement | null;
      if(x != null)x.click();
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
          localStorage["wordList"] = JSON.stringify(this.wordList);
          this.$router.go(0);
        };
        reader.readAsText(file);
      }
    },
    parseCSV(csvData: string) {
      console.log(csvData);
      const lines: string[] = csvData.split('\n');
      this.wordList = [] as { word: string; definition: string; explained: boolean; level: number }[]
      for (let i = 0; i < lines.length; i++) {
        const word: string[] = lines[i] .split(';');
        this.wordList.push({
          word: word[0],
          definition: word[1],
          explained: false,
          level: 5
        });
      }
    },
    exportToCSV(){
      this.wordList = JSON.parse(localStorage.getItem("wordList") as string);
      //todo make a header
      let header = "Word;Definition;Level;Explained\n";
      //export data
      const csvContent = "data:text/csv;charset=utf-8," + header + this.wordList.map((item) => {
        return `${item.word};${item.definition};${item.level};${item.explained}`;
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

</style>