import { ref, computed } from 'vue'

// Mock data storage - in a real app, this would be stored in a database
const userActivities = ref({
  enrolledCourses: [],
  mentorRequests: [],
  startedPaths: []
})

export function useUserActivity() {
  const enrolledCourses = computed(() => userActivities.value.enrolledCourses)
  const mentorRequests = computed(() => userActivities.value.mentorRequests)
  const startedPaths = computed(() => userActivities.value.startedPaths)
  
  const enrollInCourse = (course) => {
    const enrollment = {
      id: Date.now(),
      courseId: course.id || Date.now(),
      title: course.title,
      enrolledAt: new Date().toISOString(),
      status: 'enrolled',
      progress: 0
    }
    userActivities.value.enrolledCourses.push(enrollment)
    return enrollment
  }
  
  const sendMentorRequest = (mentor, requestData) => {
    const request = {
      id: Date.now(),
      mentorId: mentor.id || Date.now(),
      mentorName: mentor.title,
      sentAt: new Date().toISOString(),
      status: 'pending',
      message: requestData.message,
      preferredTime: requestData.preferredTime,
      meetingFrequency: requestData.meetingFrequency
    }
    userActivities.value.mentorRequests.push(request)
    return request
  }
  
  const startCareerPath = (career) => {
    const path = {
      id: Date.now(),
      careerId: career.id || Date.now(),
      title: career.title,
      startedAt: new Date().toISOString(),
      status: 'active',
      progress: 0,
      milestones: [
        { phase: '30 days', completed: false, focus: 'Close top 2 skill gaps' },
        { phase: '60 days', completed: false, focus: 'Apply skills in project context' },
        { phase: '90 days', completed: false, focus: 'Show readiness for target role' }
      ]
    }
    userActivities.value.startedPaths.push(path)
    return path
  }
  
  const updateCourseProgress = (courseId, progress) => {
    const course = userActivities.value.enrolledCourses.find(c => c.courseId === courseId)
    if (course) {
      course.progress = progress
    }
  }
  
  const updatePathProgress = (pathId, progress) => {
    const path = userActivities.value.startedPaths.find(p => p.id === pathId)
    if (path) {
      path.progress = progress
    }
  }
  
  const completeMilestone = (pathId, milestoneIndex) => {
    const path = userActivities.value.startedPaths.find(p => p.id === pathId)
    if (path && path.milestones[milestoneIndex]) {
      path.milestones[milestoneIndex].completed = true
    }
  }
  
  const clearAllActivities = () => {
    userActivities.value.enrolledCourses = []
    userActivities.value.mentorRequests = []
    userActivities.value.startedPaths = []
  }
  
  return {
    enrolledCourses,
    mentorRequests,
    startedPaths,
    enrollInCourse,
    sendMentorRequest,
    startCareerPath,
    updateCourseProgress,
    updatePathProgress,
    completeMilestone,
    clearAllActivities
  }
}
