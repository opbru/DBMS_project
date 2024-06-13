<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h1 class="text-center">Login</h1>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" v-model="email" class="form-control" id="email" placeholder="Email" required />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" v-model="password" class="form-control" id="password" placeholder="Password" required />
              </div>
              <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
  import { login } from '../services/api';

  export default {
    data() {
      return {
        email: '',
        password: '',
        token: ''
      };
    },
    methods: {
      async handleLogin() {
        try {
          const response = await login(this.email, this.password);
          this.token = response.data.access_token;
          alert('Login successful');
          // Store token in localStorage or Vuex for further use
          localStorage.setItem('token', this.token);
          this.$router.push('/set_budget_and_type'); // Change this to the next step in your workflow
        } catch (error) {
          alert('Login failed');
        }
      }
    }
  };
</script>

<style scoped>

.card-body {
  background-color: #f5f5f5; /* Light grey background */
  padding: 2rem; /* Adjust padding for spacing */
}

.btn {
  border-radius: 5px; /* Rounded corners for button */
}

.form-control {
  margin-bottom: 1.5rem; /* Adjust spacing between form elements */
}

.card {
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
}

.card-header {
  background: linear-gradient(to right, #428bca, #5cb85c); /* Gradient background */
  color: #fff; /* White text for contrast */
}

.form-label {
  display: flex; /* Align icons next to labels */
  align-items: center;
}

.form-label i {
  margin-right: 1rem; /* Space between icon and label */
  color: #ccc; /* Light grey icon color */
}

</style>
