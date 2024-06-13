<template>
  <div id="app">
    <header>
      <h1>PcHelper</h1>
    </header>

    <main>
      <h2>Welcome to PcHelper!</h2>
      <p>Your one-stop solution for building your perfect PC.</p>
      <div class="buttons">
        <router-link class="btn" to="/login">Login</router-link>
        <router-link class="btn" to="/register">Register</router-link>
      </div>
      <router-view></router-view>
    </main>

    <footer>
      <p>&copy; 2024 PcHelper. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token');
    },
  },
};

</script>

<!-- <style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style> -->

<style>
body {
  margin: 0;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  background-color: #f5f5f5;
}

#app {
  text-align: center;
  color: #2c3e50;
}

header {
  background-color: #34495e;
  padding: 10px 0;
  color: white;
}

header h1 {
  margin: 0;
}

header nav {
  margin-top: 10px;
}

header nav a {
  color: white;
  text-decoration: none;
  margin: 0 15px;
  font-size: 18px;
}

header nav a:hover {
  text-decoration: underline;
}

main {
  padding: 20px;
}

main h2 {
  font-size: 24px;
  color: #34495e;
}

main p {
  font-size: 18px;
  color: #34495e;
}

main .buttons {
  margin: 20px 0;
}

main .btn {
  display: inline-block;
  margin: 0 10px;
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #34495e;
  border-radius: 5px;
  text-decoration: none;
}

main .btn:hover {
  background-color: #2c3e50;
}

footer {
  background-color: #34495e;
  padding: 10px 0;
  color: white;
  position: fixed;
  width: 100%;
  bottom: 0;
}

footer p {
  margin: 0;
}
</style>
