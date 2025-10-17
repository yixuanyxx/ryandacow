<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <span>Employee List</span>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="createEmployee">
              <v-icon left>mdi-plus</v-icon>
              Add Employee
            </v-btn>
          </v-card-title>
          
          <v-data-table
            :headers="headers"
            :items="employees"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.actions="{ item }">
              <v-btn
                small
                color="primary"
                @click="editEmployee(item)"
              >
                Edit
              </v-btn>
              <v-btn
                small
                color="error"
                @click="deleteEmployee(item)"
                class="ml-2"
              >
                Delete
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EmployeeList',
  data() {
    return {
      employees: [],
      loading: false,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Name', value: 'name' },
        { text: 'Email', value: 'email' },
        { text: 'Phone', value: 'phone' },
        { text: 'City', value: 'city' },
        { text: 'Country', value: 'country' },
        { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  async mounted() {
    await this.fetchEmployees()
  },
  methods: {
    async fetchEmployees() {
      this.loading = true
      try {
        const response = await axios.get('/api/employees/')
        this.employees = response.data.data || []
      } catch (error) {
        console.error('Error fetching employees:', error)
      } finally {
        this.loading = false
      }
    },
    createEmployee() {
      this.$router.push('/employees/create')
    },
    editEmployee(employee) {
      this.$router.push(`/employees/edit/${employee.id}`)
    },
    async deleteEmployee(employee) {
      if (confirm(`Are you sure you want to delete ${employee.name}?`)) {
        try {
          await axios.delete(`/api/employees/${employee.id}`)
          await this.fetchEmployees()
        } catch (error) {
          console.error('Error deleting employee:', error)
        }
      }
    }
  }
}
</script>
