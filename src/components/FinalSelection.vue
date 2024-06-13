<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-3">
        <div class="state-panel">
          <div class="state-circle-f">Budget selection</div>
          <div class="state-circle-t">Component selection</div>
          <div class="state-circle-f">Result</div>
        </div>
      </div>
      <div class="col-md-9 d-flex">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h1 class="text-center">Final Selection</h1>
            </div>
            <div class="card-body">
              <ul class="list-group">
                <li v-for="component in finalSelection" :key="component.type" class="list-group-item">
                  <h5>{{ component.name }}</h5>
                  <p>Type: {{ component.type }}</p>
                  <p>Price: ${{ component.price }}</p>
                </li>
              </ul>
              <h3 class="text-center mt-4">Total Price: ${{ totalPrice }}</h3>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h1 class="text-center">Recommended GPU Upgrade</h1>
            </div>
            <div class="card-body">
              <div v-if="recommendedGpu">
                <h5>{{ recommendedGpu.better_gpu_name }}</h5>
                <p>Additional Cost: ${{ recommendedGpu.more_price }}</p>
                <p>Additional Benchmark: {{ recommendedGpu.more_benchmark }}</p>
                <p>C/P Ratio: {{ recommendedGpu.cp_ratio ? recommendedGpu.cp_ratio.toFixed(2) : 'N/A' }}</p>
              </div>
              <div v-else>
                <p>No better GPU found within remaining budget.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { finalizeSelection, recommendGpu } from '../services/api';

export default {
  data() {
    return {
      finalSelection: [],
      totalPrice: 0,
      recommendedGpu: null,
      token: localStorage.getItem('token') || '',
    };
  },
  async created() {
    try {
      const finalResponse = await finalizeSelection(this.token);
      this.finalSelection = finalResponse.data.selected_components;
      this.totalPrice = finalResponse.data.total_price;

      const recommendResponse = await recommendGpu(this.token);
      this.recommendedGpu = recommendResponse.data;
    } catch (error) {
      console.error('Failed to fetch final selection or recommended GPU:', error);
    }
  },
};
</script>

<style scoped>
.col-md-3 {
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

.state-circle-t,
.state-circle-f {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 20px;
}

.state-circle-t {
  background-color: #34495e;
}

.state-circle-f {
  background-color: #666666;
}

.col-md-9 {
  display: flex;
}

.col-md-6 {
  padding: 0 10px;
  width: 500px;
}
</style>
