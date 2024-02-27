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
      word: "Ubiquitous",
      definition: "Existing or being everywhere at the same time",
      explained: false,
      level: 5,
      lastPracticing: 0
    },
      {word: "Sycophant", definition: "A person who acts obsequiously towards someone important", explained: false, level: 5,
        lastPracticing: 0},
      {word: "Ephemeral", definition: "Lasting for a very short time", explained: false, level: 5,
        lastPracticing: 0}];
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