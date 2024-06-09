<template>
  <div class="container" >
    <input v-model="userName" placeholder="user" type="hidden"/>
    <div class="word-card" :class="{ 'hidden': learnedAll}">
      <div class="word" id="word">{{ currentWord }}</div>
      <div class="definition" id="definition">{{ currentDefinition }}</div>
    </div>
    <p class = "paragraph" :class="{ 'hidden': !learnedAll}"> You are the best
       </p>
    <RouterLink to="/practicing" class="button green_button" :class="{ 'hidden': !learnedAll}">Procvičování</RouterLink>
  <button @click="showNextWord" class="button green_button"  :class="{ 'hidden': learnedAll}">Chápu to!</button>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue";

  interface WordListItem {
    word: string;
    definition: string;
    explained: boolean;
    level: number;
    lastPracticing: number;
  }
  interface WordListFromDBItem {
    Word: string;
    Definition: string;
    Explained: string;
    Level: string;
  }

  export default defineComponent({
    name: "Learning",
    data() {
      return {
        wordList: [ ] as WordListItem[],
        learnedAll: false,
        userName: 'premek@man.eu.com'
      };
    },
    computed: {
      currentWord(){
        if(this.wordList[this.currentIndex]==undefined) {
          this.loadNewWords();
          this.learnedAll = true
          return null;
        }
        return this.wordList[this.currentIndex].word;
      },
      currentDefinition(){
        if(this.wordList[this.currentIndex]==undefined)return null;
        return this.wordList[this.currentIndex].definition;
      },
      currentIndex(){
        return this.wordList.indexOf(this.wordList.filter(function(element){ return !element.explained;})[0]);
      }
    },
    methods: {
      showNextWord() {
        this.wordList[this.currentIndex].explained = true;
        this.setWordLevel(this.wordList[this.currentIndex])
        this.saveWordList()
      },
      setWordLevel(word: WordListItem){
        const apiEndpoint = '/ setWordLevel.php';
        const postData = {
          email: this.userName,
          word:word.word,
          level: word.level,
          explained: word.explained?1:0
        };
        const requestOptions = {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
                // You may need to include additional headers like authentication headers
              },
          body: JSON.stringify(postData)
        };
        fetch(apiEndpoint, requestOptions)
            .then(response => {
              if (!response.ok) {
                throw new Error(`Error: ${response.status} - ${response.statusText}`);
              }
              if (response.ok) {
                console.log("Word was saved succesfully");
              }
            });
      },
      loadNewWords() {
        const apiEndpoint = '/getWords.php';
        const postData = {
          email: this.userName
        };
        const requestOptions = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
            // You may need to include additional headers like authentication headers
          },
          body: JSON.stringify(postData)
        };

        fetch(apiEndpoint, requestOptions)
            .then(response => {
              if (!response.ok) {
                throw new Error(`Error: ${response.status} - ${response.statusText}`);
              }
              return response.json() as Promise<WordListFromDBItem[]>;
            })
            .then(data => {
              // Assuming the response is an array of objects with properties word, definition, explained, and level
              data.forEach(item => {
                console.log("Prepare word...");
                console.log(item);
                if (!this.wordList.some(w => w.word === item.Word)) {
                  console.log("Add word...");
                  let intValue = parseInt(item.Level, 10);
                  if (isNaN(intValue)) {
                    intValue = 5;
                  }
                  // Add a new object to the wordList array
                  this.wordList.push({
                    word: item.Word,
                    definition: item.Definition,
                    explained: item.Explained == "1",
                    level: intValue,
                    lastPracticing: 0
                  });
                }
              });
              this.saveWordList();

              // Print or use the updated wordList
              console.log('Updated Word List:', this.wordList);
            })
            .catch(error => {
              console.error('Fetch error:', error);
            });
      },
      saveWordList(){
        localStorage["wordList"] = JSON.stringify(this.wordList);
        //this.$router.go(0);
      },
    },
    beforeMount: function () {
      if (localStorage.getItem("wordList") === null) {
        this.wordList = [{
          word: "H",
          definition: "Vodík",
          explained: false,
          level: 5,
          lastPracticing: 0
        },  
            {word: "He", definition: "Helium", explained: false, level: 5, lastPracticing: 0},
            {word: "Li", definition: "Lithium", explained: false, level: 5, lastPracticing: 0},
            {word: "Be", definition: "Beryllium", explained: false, level: 5, lastPracticing: 0},
            {word: "B", definition: "Bor", explained: false, level: 5, lastPracticing: 0},
            {word: "C", definition: "Uhlík", explained: false, level: 5, lastPracticing: 0},
            {word: "N", definition: "Dusík", explained: false, level: 5, lastPracticing: 0},
            {word: "O", definition: "Kyslík", explained: false, level: 5, lastPracticing: 0},
            {word: "F", definition: "Fluor", explained: false, level: 5, lastPracticing: 0},
            {word: "Ne", definition: "Neon", explained: false, level: 5, lastPracticing: 0},
            {word: "Na", definition: "Sodík", explained: false, level: 5, lastPracticing: 0},
            {word: "Mg", definition: "Hořčík", explained: false, level: 5, lastPracticing: 0},
            {word: "Al", definition: "Hliník", explained: false, level: 5, lastPracticing: 0},
            {word: "Si", definition: "Křemík", explained: false, level: 5, lastPracticing: 0},
            {word: "P", definition: "Fosfor", explained: false, level: 5, lastPracticing: 0},
            {word: "S", definition: "Síra", explained: false, level: 5, lastPracticing: 0},
            {word: "Cl", definition: "Chlor", explained: false, level: 5, lastPracticing: 0},
            {word: "Ar", definition: "Argon", explained: false, level: 5, lastPracticing: 0},
            {word: "K", definition: "Draslík", explained: false, level: 5, lastPracticing: 0},
            {word: "Ca", definition: "Vápník", explained: false, level: 5, lastPracticing: 0},
            {word: "Sc", definition: "Skandium", explained: false, level: 5, lastPracticing: 0},
            {word: "Ti", definition: "Titan", explained: false, level: 5, lastPracticing: 0},
            {word: "V", definition: "Vanad", explained: false, level: 5, lastPracticing: 0},
            {word: "Cr", definition: "Chrom", explained: false, level: 5, lastPracticing: 0},
            {word: "Mn", definition: "Mangan", explained: false, level: 5, lastPracticing: 0},
            {word: "Fe", definition: "Železo", explained: false, level: 5, lastPracticing: 0},
            {word: "Co", definition: "Kobalt", explained: false, level: 5, lastPracticing: 0},
            {word: "Ni", definition: "Nikl", explained: false, level: 5, lastPracticing: 0},
            {word: "Cu", definition: "Měď", explained: false, level: 5, lastPracticing: 0},
            {word: "Zn", definition: "Zinek", explained: false, level: 5, lastPracticing: 0},
            {word: "Ga", definition: "Gallium", explained: false, level: 5, lastPracticing: 0},
            {word: "Ge", definition: "Germanium", explained: false, level: 5, lastPracticing: 0},
            {word: "As", definition: "Arsen", explained: false, level: 5, lastPracticing: 0},
            {word: "Se", definition: "Selen", explained: false, level: 5, lastPracticing: 0},
            {word: "Br", definition: "Brom", explained: false, level: 5, lastPracticing: 0},
            {word: "Kr", definition: "Krypton", explained: false, level: 5, lastPracticing: 0},
            {word: "Rb", definition: "Rubidium", explained: false, level: 5, lastPracticing: 0},
            {word: "Sr", definition: "Stroncium", explained: false, level: 5, lastPracticing: 0},
            {word: "Y", definition: "Yttrium", explained: false, level: 5, lastPracticing: 0},
            {word: "Zr", definition: "Zirkonium", explained: false, level: 5, lastPracticing: 0},
            {word: "Nb", definition: "Niob", explained: false, level: 5, lastPracticing: 0},
            {word: "Mo", definition: "Molybden", explained: false, level: 5, lastPracticing: 0},
            {word: "Tc", definition: "Technecium", explained: false, level: 5, lastPracticing: 0},
            {word: "Ru", definition: "Ruthenium", explained: false, level: 5, lastPracticing: 0},
            {word: "Rh", definition: "Rhodium", explained: false, level: 5, lastPracticing: 0},
            {word: "Pd", definition: "Palladium", explained: false, level: 5, lastPracticing: 0},
            {word: "Ag", definition: "Stříbro", explained: false, level: 5, lastPracticing: 0},
            {word: "Cd", definition: "Kadmium", explained: false, level: 5, lastPracticing: 0},
            {word: "In", definition: "Indium", explained: false, level: 5, lastPracticing: 0},
            {word: "Sn", definition: "Cín", explained: false, level: 5, lastPracticing: 0}
        ];
      } else{
        this.wordList = JSON.parse(localStorage.getItem("wordList") as string);
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
.hidden{
  display: none;
}
.paragraph{
  color: #ababab;
  background: black;
  padding: 10px;
  margin: 10px;
  font-size: larger;
  font-weight: bold;
}
</style>