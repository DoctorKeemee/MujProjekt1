<template>
  <div class="container" >
    <div class="word-card" >
      <div class="definition" id="definition">{{ currentDefinition }}</div>
    </div>
    <div class="word-card" v-for="option in randomOptionsWords(3)" >
      <button @click = "deliverAnswer(option)" class="word button" :class="{ 'green_button': isSuccess && isTheWordCorrect(option), 'red_button': isFailed && !isTheWordCorrect(option) && isTheWordLastAnswer(option) }" id="word">{{ option }}</button>
    </div>
    <button class="next-word" :class="{ 'hidden': !isSuccess && !isFailed }" @click="nextWord()">Next word</button>
  </div>

</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Practicing",
  data() {
    return {
    wordList: [ ] as { word: string; definition: string; explained: boolean; level: number; lastPracticing: number }[],
    options: [] as string[],
      isSuccess: false,
      isFailed: false,
      frozeCurrentIndex: -1,
      repeatingCount: 2,
      lastAnswer: null as string | null
  };
  },
  computed: {
  currentWord(){
    if (this.frozeCurrentIndex<0)return "";
    return this.wordList[this.frozeCurrentIndex].word;
  },
  currentDefinition(){
    if (this.frozeCurrentIndex<0)return "";
    return this.wordList[this.frozeCurrentIndex].definition;
  },
    currentIndex(){
    let candidates = this.wordList.filter(function(element){ return element.explained && element.level == null;});
    if(candidates.length==0){
      candidates = this.wordList.filter(function(element){ return element.explained && element.level < 10;});
    }
    if(candidates.length==0){
      this.$router.push({ path: '/learning' });
      return -1;
    }
    candidates.sort(function(a, b){return a.level - b.level});
    candidates = candidates.slice(0, this.repeatingCount);
    console.log(candidates);
    candidates.sort(function(a, b){return a.lastPracticing - b.lastPracticing});
    console.log(candidates);
    return this.wordList.indexOf(candidates[0]);
  }},
  methods: {
    randomOptionsWords(numberOptions: number){
      if (this.frozeCurrentIndex<0)return [];
      let allSelectedWords = {} as { [index: number]: string[] }

      if (localStorage.getItem("selectedWords") === null) {
      }else{
        allSelectedWords = JSON.parse(localStorage.getItem("selectedWords") as string) as { [index: number]: string[] }
        if(this.frozeCurrentIndex in allSelectedWords) {
          return allSelectedWords[this.frozeCurrentIndex];
        }
      }

      if (numberOptions > this.wordList.length) {
        console.log("n must be less than the length of the list.");
        throw new Error("n must be less than the length of the list.")
      }
      let selectedWordsIndexes = [] as number[];
      selectedWordsIndexes.push(this.frozeCurrentIndex);

      while (selectedWordsIndexes.length <= numberOptions - 1){
        const randomIndex = Math.floor(Math.random() * this.wordList.length);
        if(!selectedWordsIndexes.includes(randomIndex)){
          selectedWordsIndexes.push(randomIndex);
        }
      }
      //hodím si kostkou jestli má být druhý prvek na místě prvního nebo naopak
      selectedWordsIndexes.sort(() => Math.random()-0.5);

      let selectedWords = [] as string[];
      for (let i = 0; i < selectedWordsIndexes.length; i++) {
        console.log(i);
        selectedWords.push(this.wordList[selectedWordsIndexes[i]].word);
      }
      allSelectedWords[this.frozeCurrentIndex] = selectedWords;
      localStorage["selectedWords"] = JSON.stringify(allSelectedWords);
    return selectedWords;

  },
    isTheWordCorrect(word:string){
      return word == this.currentWord;
    },
    isTheWordLastAnswer(word:string){
      return word == this.lastAnswer;
    },
    deliverAnswer(word:string){
      if(!this.isSuccess && !this.isFailed) {
        console.log(this.isTheWordCorrect(word));
        this.lastAnswer = word;
        if (this.isTheWordCorrect(word)) {
          this.wordList[this.frozeCurrentIndex].level++;
          this.isSuccess = true;
        } else {
          this.wordList[this.frozeCurrentIndex].level--;
          this.isFailed = true;
          console.log(this.wordList[this.frozeCurrentIndex].level);
        }
        this.saveWordList();
      }
    },
    saveWordList(){
      for (let i = 0; i < this.wordList.length; i++) {
        this.wordList[i].lastPracticing--;
      }
      this.wordList[this.frozeCurrentIndex].lastPracticing = 0;
      localStorage["wordList"] = JSON.stringify(this.wordList);
    },
    nextWord(){
      this.$router.go(0);
    }
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
      ]
  } else{
    this.wordList = JSON.parse(localStorage.getItem("wordList") as string);
    this.frozeCurrentIndex = this.currentIndex;
  }
}
})

</script>



<style scoped>
.button{
  color: rgba(0, 0, 0, 0.99);
  font-size: larger;
  padding: 5px;
  margin: 5px;
}
.next-word{
  background: whitesmoke ;
  color: black ;
}
.green_button {
  background: greenyellow;
}
.red_button {
  background: darkred;
}
.word-card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 2px 2px 5px #aaa;
  width: 300px;
  text-align: center;
  background: #181717;
  background-repeat: no-repeat;
  background-position: right top;
  color: black;
}
.word {
  font-size: 36px;
  font-weight: bold;
}
.definition {
  color: white;
  font-weight: bold;
  margin-top: 10px;
  font-size: 18px;
}

.hidden{
  display: none;
}

</style>