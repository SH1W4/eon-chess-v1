// Lead Scoring System
const leadScoring = {
  score: 0,
  actions: [],
  sessionStart: Date.now(),
  
  // Initialize lead scoring
  init() {
    // Load existing score from localStorage
    const savedScore = localStorage.getItem('leadScore');
    if (savedScore) {
      this.score = parseInt(savedScore, 10);
    }
    
    // Load actions history
    const savedActions = localStorage.getItem('leadActions');
    if (savedActions) {
      this.actions = JSON.parse(savedActions);
    }
  },
  
  // Track page visit
  trackPageVisit() {
    this.trackAction('page_visit', 1);
  },
  
  // Track specific actions
  trackAction(action, points) {
    // Avoid duplicate actions in the same session
    const existingAction = this.actions.find(a => 
      a.action === action && 
      a.timestamp > this.sessionStart
    );
    
    if (!existingAction) {
      this.score += points;
      this.actions.push({
        action,
        points,
        timestamp: Date.now()
      });
      
      this.save();
      this.evaluateLead();
    }
  },
  
  // Track form submission
  trackSubmission(formData) {
    const submission = {
      ...formData,
      score: this.score,
      actions: this.actions,
      timestamp: Date.now()
    };
    
    // In a real application, this would send data to a server
    console.log('Lead submission:', submission);
    
    // Store locally for demo purposes
    localStorage.setItem('leadSubmission', JSON.stringify(submission));
  },
  
  // Save current state
  save() {
    localStorage.setItem('leadScore', this.score.toString());
    localStorage.setItem('leadActions', JSON.stringify(this.actions));
  },
  
  // Evaluate lead quality
  evaluateLead() {
    let quality = 'cold';
    
    if (this.score >= 50) {
      quality = 'hot';
    } else if (this.score >= 30) {
      quality = 'warm';
    }
    
    // Trigger different behaviors based on lead quality
    if (quality === 'hot' && !this.hasShownHotLeadOffer) {
      this.showHotLeadOffer();
    }
    
    return quality;
  },
  
  // Show special offer for hot leads
  showHotLeadOffer() {
    this.hasShownHotLeadOffer = true;
    
    // Could trigger a special modal or notification
    console.log('Hot lead detected! Score:', this.score);
  },
  
  // Get lead insights
  getInsights() {
    const totalTime = Math.round((Date.now() - this.sessionStart) / 1000);
    const quality = this.evaluateLead();
    
    return {
      score: this.score,
      quality,
      totalTime,
      actionsCount: this.actions.length,
      topActions: this.getTopActions()
    };
  },
  
  // Get most valuable actions
  getTopActions() {
    const actionSummary = {};
    
    this.actions.forEach(action => {
      if (!actionSummary[action.action]) {
        actionSummary[action.action] = {
          count: 0,
          totalPoints: 0
        };
      }
      
      actionSummary[action.action].count++;
      actionSummary[action.action].totalPoints += action.points;
    });
    
    return Object.entries(actionSummary)
      .map(([action, data]) => ({
        action,
        ...data
      }))
      .sort((a, b) => b.totalPoints - a.totalPoints)
      .slice(0, 5);
  }
};

// Initialize on load
leadScoring.init();
