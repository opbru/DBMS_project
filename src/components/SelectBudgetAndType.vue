<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-3">
        <div class="state-panel">
          <div class="state-circle-t">Budget selection</div>
          <div class="state-circle-f">Component selection</div>
          <div class="state-circle-f">Result</div>
        </div>
      </div>
      <div class="col-md-6 offset-md-3">
        <div class="card">
          <div class="card-header">
            <h1 class="text-center">Select Budget and Computer Type</h1>
          </div>
          <div class="card-body">
            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="budget" class="form-label">Budget</label>
                <input type="number" v-model="budget" class="form-control" id="budget" placeholder="Enter your budget" required />
              </div>
              <div class="mb-3">
                <label for="computer_type" class="form-label">Computer Type</label>
                <select v-model="computer_type" class="form-select" id="computer_type" required>
                  <option value="" disabled>Select a computer type</option>
                  <option value="Gaming PC">Gaming PC</option>
                  <option value="Office PC">Office PC</option>
                  <option value="Workstation">Workstation</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary w-100">Submit</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<!-- <template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h1 class="text-center">Select Budget and Computer Type</h1>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                  <label for="budget" class="form-label">Budget</label>
                  <input type="number" v-model="budget" class="form-control" id="budget" placeholder="Enter your budget" required />
                </div>
                <div class="mb-3">
                  <label for="computer_type" class="form-label">Computer Type</label>
                  <select v-model="computer_type" class="form-select" id="computer_type" required>
                    <option value="" disabled>Select a computer type</option>
                    <option value="Gaming PC">Gaming PC</option>
                    <option value="Office PC">Office PC</option>
                    <option value="Workstation">Workstation</option>
                  </select>
                </div>
                <button type="submit" class="btn btn-primary w-100">Submit</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template> -->

  <script>
  import { setBudgetAndType } from '../services/api';

  export default {
    data() {
      return {
        budget: '',
        computer_type: '',
        token: localStorage.getItem('token') || '',
        currentState: 'Budget Selection',
      };
    },
    methods: {
      async handleSubmit() {
        try {
          await setBudgetAndType(this.budget, this.computer_type, this.token);
          alert('Budget and computer type set successfully');
          this.currentState = 'Product Selection'; // Update state
          this.$router.push('/get_cpu_options'); // Change this to the next step in your workflow
        } catch (error) {
          alert('Failed to set budget and computer type');
        }
      },
    },
  };
  </script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
}  
.col-md-3{
  background-color: #aaaaaa;
  height: fit-content;
  width: fit-content;
  border-radius: 50px;
}

.state-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 10px;
}

.state-circle-t {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #34495e;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 20px;
}
.state-circle-f {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #666666;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 20px;
}
.card {
  width: 100%;
}

.card-header {
  background-color: #34495e;
  color: white;
}

.card-header h1 {
  margin: 0;
}

.card-body {
  padding: 20px;
}
</style>

