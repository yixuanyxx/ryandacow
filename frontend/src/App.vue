<template>
  <v-app>
    <v-app-bar color="primary" dark>
      <v-app-bar-title>Employee Management System</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn to="/" text>Home</v-btn>
      <v-btn to="/employees" text>Employees</v-btn>
    </v-app-bar>
    
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App'
}
</script>
