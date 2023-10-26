<template>
  <v-container class="text-center">
    <v-img class="mx-auto" height="200px" max-width="100%" width="300px" src="../assets/img/chatnoir-icon.svg"/>
    <section>

      <h1 class="text-h3 text-sm-h3 py-4 mt-10">
        ChatCat - A Research Tool for Generative Retrieval Systems
      </h1>
      <p class="mx-auto py-4 tira-explanation">
        We present ChatCat, a software suite for conducting laboratory experiments and user studies with generative
        retrieval systems.
      </p>
      <v-row class="d-flex justify-center py-4">
        <v-col cols="auto">
          <v-btn color="error" href="/c" min-width="228" rel="noopener noreferrer" size="x-large" variant="flat">
            <v-icon icon="mdi-chat-outline" size="large" start/>
            Get Started
          </v-btn>
        </v-col>
        <!--        <v-col cols="auto text-primary">-->
        <!--          <v-btn href="https://webis.de/downloads/publications/papers/potthast_2019p.pdf" min-width="228" rel="noopener noreferrer" size="x-large" variant="outlined">-->
        <!--            <v-icon size="large" start>-->
        <!--              <v-img src="@/assets/logo.svg" />-->
        <!--            </v-icon>-->
        <!--            Why TIRA?-->
        <!--          </v-btn>-->
        <!--        </v-col>-->
        <v-col cols="auto">
          <v-btn class="home-button" href="https://github.com/chatnoir-eu/chatnoir-chat" min-width="228"
                 rel="noopener noreferrer" size="x-large" variant="flat">
            <v-icon icon="mdi-github" size="large" start/>
            GitHub
          </v-btn>
        </v-col>
      </v-row>
      <!--      <v-row class="d-flex align-center justify-center">-->
      <!--        <v-col cols="auto">-->
      <!--          <v-btn disabled href="" min-width="164" rel="noopener noreferrer" variant="text">-->
      <!--            <v-icon icon="mdi-view-dashboard" size="large" start/>-->
      <!--            My tasks-->
      <!--          </v-btn>-->
      <!--        </v-col>-->
      <!--        <v-col cols="auto">-->
      <!--          <v-btn href="/categories" min-width="164" rel="noopener noreferrer" variant="text">-->
      <!--            <v-icon icon="mdi-account-group" size="large" start/>-->
      <!--            Help-->
      <!--          </v-btn>-->
      <!--        </v-col>-->
      <!--      </v-row>-->
    </section>
  </v-container>
</template>

<style scoped>
.tira-explanation {
  font-size: 1.25rem;
  font-weight: 300;
  max-width: 525px;
}

.home-button {
  color: #fff;
  background: #000;
}

.home-button:hover {
  color: #fff;
  background: #000;
}

.home-button:visited {
  color: #fff;
  background: #000;
}
</style>
<script setup lang="ts">
</script>
