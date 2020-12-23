<template>
  <div class="report-item">
    <div class="report-normal" v-if="contentIsEmpty">
      此用例未发现异常
    </div>
    <div v-else>
      <div v-for="report in reports" :key="report.test_id">
        <case-report-item :report='report.content' :id="report.test_id"/>
      </div>
    </div>
  </div>
</template>

<script>
import { getReport } from '../api'
import CaseReportItem from './CaseReportItem'

export default {
  props: {
    caseId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      reports: null
    }
  },
  computed: {
    contentIsEmpty() {
      if (this.reports && this.reports.length == 0) return true
      if (!this.reports) return true
      return false
    }
  },
  mounted() {
    let jobId = this.$route.params.id
    getReport(jobId, this.caseId).then(resp => {
      this.reports = resp.data.reports
      console.log(this.reports)
    })
  },
  components: {
    CaseReportItem
  }
}
</script>

<style lang="scss">
.report-item {
  .report-normal {
    padding: 8px 0;
    text-align: center;
    color: #bbbbbb;
  }
}
</style>
