<template>
  <div>Vítejte na naší interaktivní platformě pro procvičování slovní zásoby! Naše webové stránky jsou navrženy tak, aby vám pomohly zlepšit vaše jazykové dovednosti a pozvednout vaši slovní zásobu na vyšší úroveň. Ať už se učíte nový jazyk, připravujete se na zkoušky, nebo se prostě jen snažíte udržet své jazykové schopnosti na špičkové úrovni - naše cvičení na slovní zásobu poskytují efektivní a příjemný způsob, jak dosáhnout svých cílů. Věříme, že učení má být zábavné a motivující, a proto se snažíme do procesu rozšiřování slovní zásoby vnést lehkost a radost.</div>
  <div class="align_l">
    <h1  class="align_c">Nápověda</h1>
    <ul>
      <li><b>Učení</b> - V záložce učení jsou slovíčka, které se v aplikaci naučíte a když je umíte, tak kliknete na "Chápu to" a aplikace vás přenese do záložky "Procvičování".</li>
      <li><b>Procvičování</b> - V záložce procvičování jsou Vaše slovíčka, která chápete a můžete si je zde procvičovat. Když význam zodpovíte správně, tak se vám k němu algoritmus přičte 1 bod (začínáte na 10 bodech), když ho zodpovíte špatně, 1 bod se odečte. Systém vám vždy k procvičení předloží slovíčko s nejmenším počtem bodů.</li>
      <li><b>Data managemant</b> - V záložce Data managemant máte dvě možnosti, buď si naimportujete svoje vlastní slovíčka nebo si ty, co momentálně procvičujete vyexportujete.</li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  name: "Home"
})
</script>

<style scoped>
.align_l {
  text-align: left;
}
.align_c {
  text-align: center;
}

ul {
  list-style: disc;
}

h1 {
  font-size: 200%;
  font-weight: 400;
}

</style>

