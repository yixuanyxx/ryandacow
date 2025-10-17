<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            {{ isEdit ? 'Edit Employee' : 'Create New Employee' }}
          </v-card-title>
          
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="employee.name"
                    label="Full Name"
                    :rules="nameRules"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="employee.email"
                    label="Email"
                    type="email"
                    :rules="emailRules"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
              
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="employee.phone"
                    label="Phone"
                    :rules="phoneRules"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="employee.address"
                    label="Address"
                    :rules="addressRules"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
              
              <v-row>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="employee.city"
                    label="City"
                    :rules="cityRules"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="employee.state"
                    label="State"
                    :rules="stateRules"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="employee.zip"
                    label="ZIP Code"
                    :rules="zipRules"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
              
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="employee.country"
                    label="Country"
                    :rules="countryRules"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="grey" @click="cancel">
              Cancel
            </v-btn>
            <v-btn 
              color="primary" 
              @click="saveEmployee"
              :disabled="!valid"
              :loading="loading"
            >
              {{ isEdit ? 'Update' : 'Create' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EmployeeForm',
  props: {
    id: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      valid: false,
      loading: false,
      employee: {
        name: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        state: '',
        zip: '',
        country: ''
      },
      nameRules: [
        v => !!v || 'Name is required'
      ],
      emailRules: [
        v => !!v || 'Email is required',
        v => /.+@.+\..+/.test(v) || 'Email must be valid'
      ],
      phoneRules: [
        v => !!v || 'Phone is required'
      ],
      addressRules: [
        v => !!v || 'Address is required'
      ],
      cityRules: [
        v => !!v || 'City is required'
      ],
      stateRules: [
        v => !!v || 'State is required'
      ],
      zipRules: [
        v => !!v || 'ZIP code is required'
      ],
      countryRules: [
        v => !!v || 'Country is required'
      ]
    }
  },
  computed: {
    isEdit() {
      return !!this.id
    }
  },
  async mounted() {
    if (this.isEdit) {
      await this.fetchEmployee()
    }
  },
  methods: {
    async fetchEmployee() {
      this.loading = true
      try {
        const response = await axios.get(`/api/employees/${this.id}`)
        this.employee = response.data.data
      } catch (error) {
        console.error('Error fetching employee:', error)
        this.$router.push('/employees')
      } finally {
        this.loading = false
      }
    },
    async saveEmployee() {
      if (this.$refs.form.validate()) {
        this.loading = true
        try {
          if (this.isEdit) {
            await axios.put(`/api/employees/${this.id}`, this.employee)
          } else {
            await axios.post('/api/employees/create', this.employee)
          }
          this.$router.push('/employees')
        } catch (error) {
          console.error('Error saving employee:', error)
        } finally {
          this.loading = false
        }
      }
    },
    cancel() {
      this.$router.push('/employees')
    }
  }
}
</script>
