<template>
  <div class="container" >
    <div class="word-card" >
      <div class="definition" id="definition">{{ currentDefinition }}</div>
    </div>
    <div class="word-card" v-for="option in randomOptionsWords(3)" >
      <button @click = "IsTheWordCorrect(option)" class="word button" :class="{ 'green_button': isActive }" id="word">{{ option }}</button>
    </div>
  </div>

</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "Practicing",
  data() {
    return {
    wordList: [
      { word: "Ubiquitous", definition: "Existing or being everywhere at the same time", explained: false },
      { word: "Sycophant", definition: "A person who acts obsequiously towards someone important", explained: false  },
      { word: "Ephemeral", definition: "Lasting for a very short time", explained: false  }
    ] as { word: string; definition: string; explained: boolean }[],
    currentIndex: ref(0),
    options: [] as string[],
      isActive: false,
      hasError: false
  };
  },
  computed: {
  currentWord(){
    return this.wordList[this.currentIndex].word;
  },
  currentDefinition(){
    return this.wordList[this.currentIndex].definition;
  }},
  methods: {
    randomOptionsWords(numberOptions: number){
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
      selectedWordsIndexes.sort(() => Math.random()-0.5)

      var selectedWords = [] as string[];
      for (let i = 0; i < selectedWordsIndexes.length; i++) {
        console.log(i);
        selectedWords.push(this.wordList[selectedWordsIndexes[i]].word);
      }
    return selectedWords;

  },
    IsTheWordCorrect(word:string){
      console.log(word==this.currentWord);
      if (word == this.currentWord){this.isActive = true}
    }
},
})

</script>



<style scoped>
.button{
  color: antiquewhite;
  font-size: larger;
  padding: 5px;
  margin: 5px;
}
.green_button {
  background: green;
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

</style>