<template>
  <div id="print-section" class="offer-letter-container p-4 p-md-5 bg-white shadow-lg rounded-4 border mx-auto">
    <!-- Letterhead -->
    <div class="d-flex flex-column flex-sm-row justify-content-between align-items-start mb-5 pb-4 border-bottom gap-4">
      <div class="company-info">
        <div class="d-flex align-items-center gap-3 mb-3">
          <div class="company-logo bg-light rounded-3 d-flex align-items-center justify-content-center p-2 border overflow-hidden" style="width: 65px; height: 65px;">
            <img v-if="companyLogo" :src="companyLogo" :alt="companyName" class="img-fluid rounded-2">
            <i v-else class="fas fa-building text-secondary opacity-50 fs-4"></i>
          </div>
          <div>
            <h4 class="fw-bold text-dark mb-0">{{ companyName }}</h4>
            <div class="small text-muted text-uppercase tracking-wider fw-medium ls-tight" style="font-size: 0.75rem;">Talent Acquisition Division</div>
          </div>
        </div>
      </div>
      <div class="text-sm-end w-100 flex-sm-shrink-1">
        <div class="text-primary fw-bold small mb-1 tracking-widest text-uppercase">Conditional Offer Letter</div>
        <div class="text-muted small">Date Issued: <strong>{{ currentDate }}</strong></div>
        <div class="small text-muted mt-1 opacity-75">ID: #OFFER-{{ Math.random().toString(36).substr(2, 6).toUpperCase() }}</div>
      </div>
    </div>

    <!-- Content Body -->
    <div class="offer-contenttext-dark">
      <div class="mb-2">
        <p class="mb-1">To,</p>
        <p class="mb-0 fs-5 fw-bold text-dark">{{ studentName }}</p>
        <p class="small text-muted opacity-75">Applicant for the Graduate Recruitment Program</p>
      </div>

      <div class="mb-4">
        <p class="mb-4">Following the recruitment process for the <strong>{{ driveTitle }}</strong> drive, we are incredibly pleased to extend this formal offer of employment to you. At <strong>{{ companyName }}</strong>, we are building a team of visionary individuals, and our recruiters were highly impressed by your skills and potential.</p>
        
        <p class="mb-0">This letter outlines the primary terms and conditions of your association with us:</p>
      </div>

      <!-- Detail Card -->
      <div class="mb-2 p-4 rounded-4 position-relative overflow-hidden">
          <div class="position-absolute top-0 start-0 w-100 h-100 opacity-5" style="pointer-events: none;"></div>
          <h6 class="fw-bold mb-4 text-primary text-uppercase small ls-tight d-flex align-items-center gap-2">
              <i class="fas fa-file-contract"></i> Appointment Framework
          </h6>
          <div class="row g-4 position-relative">
              <div class="col-sm-6">
                  <div class="detail-label small text-muted text-uppercase fw-bold opacity-75 mb-1">Designation</div>
                  <div class="text-dark fw-bold border-start border-3 border-danger ps-2">{{ driveTitle }}</div>
              </div>
              <div class="col-sm-6">
                  <div class="detail-label small text-muted text-uppercase fw-bold opacity-75 mb-1">Base Location</div>
                  <div class="text-dark fw-bold border-start border-3 border-danger ps-2">{{ location }}</div>
              </div>
              <div class="col-sm-6">
                  <div class="detail-label small text-muted text-uppercase fw-bold opacity-75 mb-1">Employment Model</div>
                  <div class="text-dark fw-bold border-start border-3 border-danger ps-2">{{ workMode || 'Full-time Hybrid' }}</div>
              </div>
              <div class="col-sm-6">
                  <div class="detail-label small text-muted text-uppercase fw-bold opacity-75 mb-1">Offered Compensation</div>
                  <div class="text-dark fw-bold border-start border-3 border-danger ps-2 text-highlight">{{ payScale }}</div>
              </div>
          </div>
      </div>

      <div class="mb-2 border-start border-3 border-primary ps-4 py-1 bg-light bg-opacity-50">
        <p class="mb-0 fst-italic text-muted small">By accepting this conditional offer, you confirm that all information provided during the recruitment process is accurate. Detailed joining instructions and a comprehensive contract will follow upon your formal acceptance.</p>
      </div>
    </div>

    <!-- Final Signature -->
    <div class="signature-block d-flex justify-content-between align-items-end mt-5 pt-4">
      <div>
        <div class="mb-4">
            <div class="text-muted small mb-0">Best Regards,</div>
            <div class="letter-signing" style="font-family: 'Brush Script MT', cursive; font-size: 1.8rem; line-height: 1;">HR Director</div>
        </div>
        <div class="fw-bold text-dark">{{ companyName }}</div>
        <div class="small text-muted tracking-wider text-uppercase" style="font-size: 0.7rem;">Head of Global Talent Acquisition</div>
      </div>
    </div>
    
    <!-- Action Bar for Digital View -->
    <div class="mt-5 pt-4 text-center d-print-none border-top">
        <div class="d-flex flex-wrap justify-content-center gap-3">
            <button @click="printLetter" class="btn btn-primary rounded-pill px-4 fw-bold shadow-sm d-flex align-items-center gap-2">
                <i class="fas fa-file-pdf"></i> Download PDF
            </button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  studentName: { type: String, required: true },
  companyName: { type: String, required: true },
  companyLogo: { type: String, default: '' },
  driveTitle: { type: String, required: true },
  location: { type: String, required: true },
  payScale: { type: String, required: true },
  workMode: { type: String, default: 'Standard Hybrid' }
})

const currentDate = computed(() => {
  return new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })
})

const printLetter = () => {
    window.print()
}
</script>

<style scoped>
.offer-letter-container {
  max-width: 850px;
  background-color: #ffffff;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: #1a1a1a;
  position: relative;
  box-shadow: 0 40px 100px rgba(0,0,0,0.1) !important;
}

.tracking-wider { letter-spacing: 0.05em; }
.tracking-widest { letter-spacing: 0.15em; }
.ls-tight { letter-spacing: -0.01em; }

.text-highlight {
  color: var(--color-primary, #781f19);
}

.offer-content p {
  margin-bottom: 1.5rem;
}

@media print {
  body * {
      visibility: hidden;
  }

  #print-section, #print-section * {
      visibility: visible;
  }

  #print-section {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
  }
}

@media (max-width: 576px) {
    .offer-letter-container {
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
}
</style>
