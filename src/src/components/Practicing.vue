<template>
  <div class="container" >
    <div class="word-card" >
      <div class="definition" id="definition">{{ currentDefinition }}</div>
    </div>
    <div class="word-card" v-for="option in randomOptionsWords(3)" >
      <button @click = "deliverAnswer(option)" class="word button" :class="{ 'green_button': isSuccess && isTheWordCorrect(option) }" id="word">{{ option }}</button>
    </div>
    <button class="next-word" :class="{ 'hidden': !isSuccess }" @click="nextWord()">Next word</button>
  </div>

</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Practicing",
  data() {
    return {
    wordList: [ ] as { word: string; definition: string; explained: boolean; level: number }[],
    options: [] as string[],
      isSuccess: false
  };
  },
  computed: {
  currentWord(){
    return this.wordList[this.currentIndex].word;
  },
  currentDefinition(){
    return this.wordList[this.currentIndex].definition;
  },
  currentIndex(){
    let candidates = this.wordList.filter(function(element){ return !element.explained;});
    candidates.sort(function(a, b){return a.level - b.level});
    return this.wordList.indexOf(candidates[0]);
  }},
  methods: {
    randomOptionsWords(numberOptions: number){
      let allSelectedWords = {} as { [index: number]: string[] }

      if (localStorage.getItem("selectedWords") === null) {
      }else{
        allSelectedWords = JSON.parse(localStorage.getItem("selectedWords") as string) as { [index: number]: string[] }
        if(this.currentIndex in allSelectedWords) {
          return allSelectedWords[this.currentIndex];
        }
      }

      if (numberOptions > this.wordList.length) {
        console.log("n must be less than the length of the list.");
        throw new Error("n must be less than the length of the list.")
      }
      let selectedWordsIndexes = [] as number[];
      selectedWordsIndexes.push(this.currentIndex);

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
      allSelectedWords[this.currentIndex] = selectedWords;
      localStorage["selectedWords"] = JSON.stringify(allSelectedWords);
    return selectedWords;

  },
    isTheWordCorrect(word:string){
      return word == this.currentWord;
    },
    deliverAnswer(word:string){
      console.log(this.isTheWordCorrect(word));
      if (this.isTheWordCorrect(word)){
        this.wordList[this.currentIndex].level++;
        this.isSuccess = true;
      }else{
        this.wordList[this.currentIndex].level--;
        console.log(this.wordList[this.currentIndex].level);
      }
      this.saveWordList();
    },
    saveWordList(){
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
      level: 5
    },
      {word: "Sycophant", definition: "A person who acts obsequiously towards someone important", explained: false, level: 5},
      {word: "Ephemeral", definition: "Lasting for a very short time", explained: false, level: 5}];
  } else{
    this.wordList = JSON.parse(localStorage.getItem("wordList") as string);
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