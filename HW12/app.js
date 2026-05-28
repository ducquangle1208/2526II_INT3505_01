/* ==========================================================================
   DEVELOPER PORTAL - APP LOGIC (HW12)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide Icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  // Initialize all components
  initTabNavigation();
  initPricingCalculator();
  initDocsNavigation();
  initCodeTabSystem();
  
  // Call initial layout alignment
  onEndpointChange();
});

/* ==========================================================================
   1. TAB NAVIGATION SYSTEM
   ========================================================================== */
function initTabNavigation() {
  const tabs = document.querySelectorAll('#navigation-tabs .tab-btn');
  
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.getAttribute('data-target');
      switchTab(targetId);
    });
  });
}

function switchTab(tabId) {
  // Hide all tab content
  const contents = document.querySelectorAll('.tab-content');
  contents.forEach(content => content.classList.remove('active'));
  
  // Deactivate all navigation buttons
  const buttons = document.querySelectorAll('#navigation-tabs .tab-btn');
  buttons.forEach(btn => {
    btn.classList.remove('active');
    btn.setAttribute('aria-selected', 'false');
  });
  
  // Show target tab content
  const targetContent = document.getElementById(tabId);
  if (targetContent) {
    targetContent.classList.add('active');
  }
  
  // Activate target navigation button
  let btnId = 'tab-btn-overview';
  if (tabId === 'tab-docs') btnId = 'tab-btn-docs';
  if (tabId === 'tab-sandbox') btnId = 'tab-btn-sandbox';
  
  const targetBtn = document.getElementById(btnId);
  if (targetBtn) {
    targetBtn.classList.add('active');
    targetBtn.setAttribute('aria-selected', 'true');
  }
  
  // Scroll to top of the page smoothly
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Global scroll helper to Calculator
function scrollToCalculator() {
  switchTab('tab-overview');
  setTimeout(() => {
    const calcElement = document.getElementById('monetization-section');
    if (calcElement) {
      calcElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, 100);
}

/* ==========================================================================
   2. DYNAMIC PRICING & HYBRID MONETIZATION CALCULATOR
   ========================================================================== */
function initPricingCalculator() {
  const slider = document.getElementById('requests-slider');
  const labelCurrent = document.getElementById('calc-requests-val');
  
  if (!slider) return;
  
  slider.addEventListener('input', () => {
    const value = parseInt(slider.value);
    
    // Format requests value label
    if (value >= 1000000) {
      labelCurrent.textContent = '1,000,000+ requests';
    } else {
      labelCurrent.textContent = value.toLocaleString('en-US') + ' requests';
    }
    
    calculatePrice(value);
  });
  
  // Trigger initial calculation
  calculatePrice(parseInt(slider.value));
}

function calculatePrice(requests) {
  const suggestedPlanVal = document.getElementById('calc-suggested-plan');
  const totalCostVal = document.getElementById('calc-total-cost');
  const breakdownText = document.getElementById('calc-breakdown-text');
  
  // Pricing plans cards elements to add active styles
  const cardFree = document.getElementById('price-card-free');
  const cardDev = document.getElementById('price-card-dev');
  const cardScale = document.getElementById('price-card-scale');
  
  // Reset card active styles
  const allCards = [cardFree, cardDev, cardScale];
  allCards.forEach(c => {
    if (c) c.style.borderColor = '';
  });

  let suggestedPlan = '';
  let totalCost = 0;
  let breakdown = '';
  
  // Calculation Logic (Hybrid Overages Pricing Optimization)
  if (requests <= 1000) {
    // Free / Sandbox Tier
    suggestedPlan = 'Sandbox / Free Plan';
    totalCost = 0;
    breakdown = 'Gói Sandbox: $0/tháng. Hạn mức: 1,000 requests. Không cho phép vượt hạn mức.';
    if (cardFree) cardFree.style.borderColor = 'var(--color-secondary)';
  } 
  else if (requests <= 50000) {
    // Standard Developer Plan flat cost
    suggestedPlan = 'Developer Plan';
    totalCost = 29;
    breakdown = 'Phí gói cố định: $29/tháng (Bao gồm tối đa 50,000 requests). Phí vượt hạn mức: $0.001/request.';
    if (cardDev) cardDev.style.borderColor = 'var(--color-primary)';
  } 
  else if (requests <= 300000) {
    // Intermediate levels: Compare Developer Tier with Overage vs Scale-up flat rate ($149)
    const devPlanOverageCost = 29 + (requests - 50000) * 0.001;
    const scaleFlatCost = 149;
    
    if (devPlanOverageCost < scaleFlatCost) {
      suggestedPlan = 'Developer Plan (Có vượt gói)';
      totalCost = devPlanOverageCost;
      breakdown = `Gói Developer: $29 + Phí vượt gói (Pay-per-call): $${((requests - 50000) * 0.001).toFixed(2)} (${(requests - 50000).toLocaleString()} requests vượt x $0.001)`;
      if (cardDev) cardDev.style.borderColor = 'var(--color-primary)';
    } else {
      suggestedPlan = 'Scale-up Plan (Tối ưu hơn)';
      totalCost = scaleFlatCost;
      breakdown = `Gói Scale-up: $149/tháng (Bao gồm 300,000 requests). Tiết kiệm hơn gói Developer ($${devPlanOverageCost.toFixed(2)}/tháng).`;
      if (cardScale) cardScale.style.borderColor = 'var(--color-secondary)';
    }
  } 
  else if (requests <= 750000) {
    // Scale-up plan with overage
    const overageRequests = requests - 300000;
    const overageFee = overageRequests * 0.0006;
    suggestedPlan = 'Scale-up Plan (Có vượt gói)';
    totalCost = 149 + overageFee;
    breakdown = `Gói Scale-up: $149 + Phí vượt gói (Pay-per-call): $${overageFee.toFixed(2)} (${overageRequests.toLocaleString()} requests vượt x $0.0006)`;
    if (cardScale) cardScale.style.borderColor = 'var(--color-secondary)';
  } 
  else {
    // Enterprise recommendation for high volumes
    suggestedPlan = 'Enterprise Plan (Custom)';
    totalCost = requests * 0.0003; // Custom dynamic mock pricing rate
    breakdown = `Gói Enterprise liên hệ riêng. Tạm tính theo rate ưu đãi: $0.0003/request x ${requests.toLocaleString()} requests. Hỗ trợ SLA 99.99%.`;
    if (cardScale) cardScale.style.borderColor = 'var(--color-primary-light)';
  }
  
  // Render values to UI
  if (suggestedPlanVal) suggestedPlanVal.textContent = suggestedPlan;
  if (totalCostVal) {
    if (suggestedPlan.includes('Enterprise')) {
      totalCostVal.textContent = 'Liên hệ';
      totalCostVal.style.color = 'var(--color-primary-light)';
    } else {
      totalCostVal.textContent = '$' + totalCost.toFixed(2);
      totalCostVal.style.color = 'var(--color-accent)';
    }
  }
  if (breakdownText) breakdownText.textContent = breakdown;
}

/* ==========================================================================
   3. STRIPE-STYLE API REFERENCE DOCUMENTATION NAVIGATION
   ========================================================================== */
function initDocsNavigation() {
  const sidebarLinks = document.querySelectorAll('.docs-sidebar .sidebar-link');
  
  sidebarLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      
      const targetSectionId = link.getAttribute('data-doc-target');
      
      // Update sidebar active link state
      sidebarLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
      
      // Switch active document content section
      const docSections = document.querySelectorAll('.docs-main .doc-section');
      docSections.forEach(sec => sec.classList.remove('active'));
      
      const targetSec = document.getElementById('doc-' + targetSectionId);
      if (targetSec) {
        targetSec.classList.add('active');
      }
    });
  });
}

/* ==========================================================================
   4. MULTI-LANGUAGE CODE SNIPPETS TABS
   ========================================================================== */
function initCodeTabSystem() {
  // Capture clicks on language buttons inside code blocks
  document.addEventListener('click', (e) => {
    if (e.target && e.target.classList.contains('code-tab-btn')) {
      const container = e.target.closest('.code-tab-container');
      if (!container) return;
      
      const targetLang = e.target.getAttribute('data-lang');
      
      // Deactivate all sibling buttons
      const buttons = container.querySelectorAll('.code-tab-btn');
      buttons.forEach(btn => btn.classList.remove('active'));
      e.target.classList.add('active');
      
      // Show/Hide matching pre elements
      const contents = container.querySelectorAll('.code-tab-content');
      contents.forEach(content => {
        if (content.getAttribute('data-lang') === targetLang) {
          content.classList.add('active');
        } else {
          content.classList.remove('active');
        }
      });
    }
  });
}

/* ==========================================================================
   5. INTERACTIVE API SANDBOX / PLAYGROUND SIMULATOR
   ========================================================================== */
function onEndpointChange() {
  const endpoint = document.getElementById('sb-endpoint').value;
  const groupSearch = document.getElementById('group-search-query');
  const groupJson = document.getElementById('group-json-body');
  const groupLimit = document.getElementById('group-limit');
  
  const jsonBodyArea = document.getElementById('sb-json-body');

  if (endpoint === 'search') {
    if (groupSearch) groupSearch.classList.remove('hidden');
    if (groupLimit) groupLimit.classList.remove('hidden');
    if (groupJson) groupJson.classList.add('hidden');
  } 
  else if (endpoint === 'recommend') {
    if (groupSearch) groupSearch.classList.add('hidden');
    if (groupLimit) groupLimit.classList.remove('hidden');
    if (groupJson) groupJson.classList.remove('hidden');
    
    // Set default body JSON for recommendations
    if (jsonBodyArea) {
      jsonBodyArea.value = JSON.stringify({
        "user_id": "usr_9988",
        "recent_viewed_ids": ["prod_001", "prod_004"],
        "limit": 2
      }, null, 2);
    }
  } 
  else if (endpoint === 'checkout') {
    if (groupSearch) groupSearch.classList.add('hidden');
    if (groupLimit) groupLimit.classList.add('hidden');
    if (groupJson) groupJson.classList.remove('hidden');
    
    // Set default body JSON for smart checkout
    if (jsonBodyArea) {
      jsonBodyArea.value = JSON.stringify({
        "items": [
          { "id": "prod_001", "quantity": 1 },
          { "id": "prod_010", "quantity": 2 }
        ],
        "shipping_address": "12 Cầu Giấy, Hà Nội, Việt Nam"
      }, null, 2);
    }
  }
}

function clearConsole() {
  const consoleBody = document.getElementById('terminal-body');
  if (consoleBody) {
    consoleBody.innerHTML = `
      <div class="terminal-line system-msg">> Console cleared. Môi trường Sandbox sẵn sàng.</div>
    `;
  }
}

function appendConsoleLine(text, cssClass = '') {
  const consoleBody = document.getElementById('terminal-body');
  if (!consoleBody) return;
  
  const line = document.createElement('div');
  line.className = 'terminal-line ' + cssClass;
  line.innerHTML = text;
  
  consoleBody.appendChild(line);
  
  // Auto scroll console to bottom
  const display = consoleBody.parentElement;
  display.scrollTop = display.scrollHeight;
}

function sendSandboxRequest() {
  const apiKey = document.getElementById('sb-api-key').value.trim();
  const endpointType = document.getElementById('sb-endpoint').value;
  const selectElement = document.getElementById('sb-endpoint');
  const selectedOption = selectElement.options[selectElement.selectedIndex];
  const method = selectedOption.getAttribute('data-method');
  
  const limitVal = parseInt(document.getElementById('sb-limit').value) || 2;
  const searchVal = document.getElementById('sb-query').value.trim();
  const jsonBodyVal = document.getElementById('sb-json-body').value.trim();
  
  // Timestamp formatting
  const now = new Date();
  const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
  
  // 1. Build and print the Request Command
  let path = '';
  if (endpointType === 'search') {
    path = `/products/search-ai?q=${encodeURIComponent(searchVal)}&limit=${limitVal}`;
  } else if (endpointType === 'recommend') {
    path = `/recommendations`;
  } else if (endpointType === 'checkout') {
    path = `/checkout/smart`;
  }
  
  appendConsoleLine(`> [${timeStr}] Gửi request: <span style="color:var(--color-primary-light);font-weight:600;">${method}</span> https://sandbox.api.aiecom.vn/v1${path}`, 'input-cmd');
  
  // Show Loading Spinner placeholder
  const spinnerId = 'spinner-' + Math.random().toString(36).substr(2, 9);
  appendConsoleLine(`<span id="${spinnerId}"><span class="spinner"></span>Đang xử lý trên server Sandbox...</span>`, 'system-msg');
  
  // Disable button to prevent spamming
  const sendBtn = document.getElementById('btn-send-sandbox');
  if (sendBtn) {
    sendBtn.disabled = true;
    sendBtn.innerHTML = `<span class="spinner"></span> Đang gửi...`;
  }

  // 2. Simulate network delay (800ms)
  setTimeout(() => {
    // Remove loading spinner
    const spinnerElement = document.getElementById(spinnerId);
    if (spinnerElement) spinnerElement.remove();
    
    // Enable request button back
    if (sendBtn) {
      sendBtn.disabled = false;
      sendBtn.innerHTML = `<i data-lucide="send"></i> Gửi Request Lên Sandbox`;
      if (typeof lucide !== 'undefined') lucide.createIcons();
    }
    
    // Authentication Validation check
    if (!apiKey) {
      appendConsoleLine(`&lt; HTTP/1.1 <span style="color:#ef4444;font-weight:600;">401 Unauthorized</span>`, 'error-res');
      const errResponse = {
        "error": "authentication_failed",
        "message": "Không tìm thấy API Key hoặc API Key không hợp lệ. Vui lòng thêm Header 'Authorization: Bearer YOUR_KEY'.",
        "documentation_url": "https://docs.aiecom.vn/errors#auth"
      };
      appendConsoleLine(JSON.stringify(errResponse, null, 2), 'error-res');
      return;
    }
    
    // Simulate endpoint matching logic
    if (endpointType === 'search') {
      simulateSearchEndpoint(searchVal, limitVal);
    } 
    else if (endpointType === 'recommend') {
      simulateRecommendEndpoint(jsonBodyVal);
    } 
    else if (endpointType === 'checkout') {
      simulateCheckoutEndpoint(jsonBodyVal);
    }
    
  }, 800);
}

/* ==========================================================================
   SANDBOX ENDPOINT SIMULATIONS
   ========================================================================== */

function simulateSearchEndpoint(query, limit) {
  appendConsoleLine(`&lt; HTTP/1.1 <span style="color:#10b981;font-weight:600;">200 OK</span>`, 'success-res');
  
  const queryLower = query.toLowerCase();
  let searchData = [];
  
  // Generate realistic product search matches based on query terms
  if (queryLower.includes('giày') || queryLower.includes('shoe') || queryLower.includes('sneaker')) {
    searchData = [
      {
        "id": "prod_001",
        "name": "Giày Chạy Bộ Nam SwiftRun Pro v3",
        "category": "Footwear",
        "price": 1250000,
        "color": "Red",
        "ai_score": 0.985,
        "stock": 42
      },
      {
        "id": "prod_004",
        "name": "Giày Sneaker Thời Trang Crimson Edge",
        "category": "Footwear",
        "price": 890000,
        "color": "Crimson Red",
        "ai_score": 0.892,
        "stock": 15
      },
      {
        "id": "prod_008",
        "name": "Giày Sandal Thể Thao Active X",
        "category": "Footwear",
        "price": 450000,
        "color": "Black/Grey",
        "ai_score": 0.741,
        "stock": 30
      }
    ];
  } 
  else if (queryLower.includes('điện thoại') || queryLower.includes('iphone') || queryLower.includes('phone') || queryLower.includes('samsung')) {
    searchData = [
      {
        "id": "prod_020",
        "name": "Điện Thoại Thông Minh Infinity S24",
        "category": "Electronics",
        "price": 21990000,
        "color": "Titanium Grey",
        "ai_score": 0.991,
        "stock": 8
      },
      {
        "id": "prod_021",
        "name": "Điện Thoại SmartPhone AI Lite v2",
        "category": "Electronics",
        "price": 6490000,
        "color": "Neon Blue",
        "ai_score": 0.854,
        "stock": 25
      }
    ];
  } 
  else {
    // Default general mock results
    searchData = [
      {
        "id": "prod_010",
        "name": "Tất Thể Thao SwiftPerformance",
        "category": "Accessories",
        "price": 95000,
        "color": "White",
        "ai_score": 0.654,
        "stock": 120
      },
      {
        "id": "prod_012",
        "name": "Bình Nước Giữ Nhiệt Vacuum Flask",
        "category": "Accessories",
        "price": 320000,
        "color": "Matte Black",
        "ai_score": 0.612,
        "stock": 88
      }
    ];
  }
  
  // Slice to respect limit parameter
  const finalResults = searchData.slice(0, Math.min(limit, searchData.length));
  
  const successResponse = {
    "status": "success",
    "query": query,
    "matched_count": finalResults.length,
    "ai_engine": "ECom-SemanticSearch-v2.1",
    "data": finalResults
  };
  
  appendConsoleLine(JSON.stringify(successResponse, null, 2), 'success-res');
}

function simulateRecommendEndpoint(bodyJsonText) {
  let bodyObj = {};
  
  // 1. JSON parsing check
  try {
    bodyObj = JSON.parse(bodyJsonText);
  } catch (e) {
    appendConsoleLine(`&lt; HTTP/1.1 <span style="color:#ef4444;font-weight:600;">400 Bad Request</span>`, 'error-res');
    const errRes = {
      "error": "invalid_json_body",
      "message": "Không thể parse body JSON của request. Lỗi cú pháp JSON: " + e.message,
    };
    appendConsoleLine(JSON.stringify(errRes, null, 2), 'error-res');
    return;
  }
  
  // 2. Validate mandatory parameters
  if (!bodyObj.user_id) {
    appendConsoleLine(`&lt; HTTP/1.1 <span style="color:#ef4444;font-weight:600;">422 Unprocessable Entity</span>`, 'error-res');
    const errRes = {
      "error": "missing_required_parameter",
      "message": "Thiếu trường 'user_id' bắt buộc trong body JSON.",
      "code": 422
    };
    appendConsoleLine(JSON.stringify(errRes, null, 2), 'error-res');
    return;
  }
  
  appendConsoleLine(`&lt; HTTP/1.1 <span style="color:#10b981;font-weight:600;">200 OK</span>`, 'success-res');
  
  const limit = bodyObj.limit || 2;
  const mockRecs = [
    {
      "id": "prod_010",
      "name": "Tất Thể Thao SwiftPerformance",
      "category": "Accessories",
      "price": 95000,
      "recommend_reason": "Thường được mua kèm với các sản phẩm giày thể thao SwiftRun",
      "score": 0.957
    },
    {
      "id": "prod_012",
      "name": "Bình Nước Giữ Nhiệt Vacuum Flask",
      "category": "Accessories",
      "price": 320000,
      "recommend_reason": "Dựa trên sở thích xem danh mục Đồ Thể Thao của bạn",
      "score": 0.815
    },
    {
      "id": "prod_004",
      "name": "Giày Sneaker Thời Trang Crimson Edge",
      "category": "Footwear",
      "price": 890000,
      "recommend_reason": "Nằm trong danh mục sản phẩm hot có màu đỏ bạn vừa xem",
      "score": 0.762
    }
  ];
  
  const finalResults = mockRecs.slice(0, Math.min(limit, mockRecs.length));
  
  const successResponse = {
    "status": "success",
    "user_id": bodyObj.user_id,
    "recommendation_engine": "ECom-Recs-v4.2-Live",
    "data": finalResults
  };
  
  appendConsoleLine(JSON.stringify(successResponse, null, 2), 'success-res');
}

function simulateCheckoutEndpoint(bodyJsonText) {
  let bodyObj = {};
  
  // 1. JSON parsing check
  try {
    bodyObj = JSON.parse(bodyJsonText);
  } catch (e) {
    appendConsoleLine(`&lt; HTTP/1.1 <span style="color:#ef4444;font-weight:600;">400 Bad Request</span>`, 'error-res');
    const errRes = {
      "error": "invalid_json_body",
      "message": "Không thể parse body JSON của request. Lỗi cú pháp JSON: " + e.message,
    };
    appendConsoleLine(JSON.stringify(errRes, null, 2), 'error-res');
    return;
  }
  
  // 2. Validate mandatory parameters
  if (!bodyObj.items || !Array.isArray(bodyObj.items) || bodyObj.items.length === 0) {
    appendConsoleLine(`&lt; HTTP/1.1 <span style="color:#ef4444;font-weight:600;">422 Unprocessable Entity</span>`, 'error-res');
    const errRes = {
      "error": "missing_required_parameter",
      "message": "Yêu cầu mảng 'items' chứa ít nhất 1 sản phẩm có id và quantity.",
      "code": 422
    };
    appendConsoleLine(JSON.stringify(errRes, null, 2), 'error-res');
    return;
  }
  
  if (!bodyObj.shipping_address) {
    appendConsoleLine(`&lt; HTTP/1.1 <span style="color:#ef4444;font-weight:600;">422 Unprocessable Entity</span>`, 'error-res');
    const errRes = {
      "error": "missing_required_parameter",
      "message": "Thiếu trường 'shipping_address' để AI định giá chi phí vận chuyển.",
      "code": 422
    };
    appendConsoleLine(JSON.stringify(errRes, null, 2), 'error-res');
    return;
  }
  
  // 3. Dynamic Calculation simulation
  appendConsoleLine(`&lt; HTTP/1.1 <span style="color:#10b981;font-weight:600;">200 OK</span>`, 'success-res');
  
  let subtotal = 0;
  bodyObj.items.forEach(item => {
    // Generate mock price values based on product ID
    let price = 150000; // default mock price
    if (item.id === 'prod_001') price = 1250000;
    if (item.id === 'prod_010') price = 95000;
    if (item.id === 'prod_012') price = 320000;
    
    subtotal += price * (item.quantity || 1);
  });
  
  const discount = subtotal > 1000000 ? 50000 : 0;
  const isHNOrHCM = bodyObj.shipping_address.toLowerCase().includes('hà nội') || bodyObj.shipping_address.toLowerCase().includes('hồ chí minh') || bodyObj.shipping_address.toLowerCase().includes('hcm');
  const shippingFee = isHNOrHCM ? 15000 : 35000;
  const total = subtotal + shippingFee - discount;
  
  const successResponse = {
    "status": "success",
    "order_valuation": {
      "subtotal": subtotal,
      "shipping_fee": shippingFee,
      "discount": discount,
      "total": total,
      "currency": "VND"
    },
    "ai_applied_insights": {
      "applied_coupon": discount > 0 ? "AI_ECOM_BIG_SAVER_50K" : "AI_ECOM_STANDARD_PRICING",
      "savings_reason": discount > 0 ? "Giảm giá 50.000đ tự động cho đơn hàng giá trị cao từ 1.000.000đ" : "Đơn chưa đạt điều kiện tối ưu voucher đặc biệt",
      "suggested_cross_sell": {
        "id": "prod_010",
        "name": "Tất Thể Thao SwiftPerformance",
        "discounted_price": 50000,
        "cross_sell_message": "Thêm tất thể thao SwiftPerformance chỉ với 50.000đ (tiết kiệm 45.000đ)!"
      }
    }
  };
  
  appendConsoleLine(JSON.stringify(successResponse, null, 2), 'success-res');
}
