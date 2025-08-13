// Alpine.js Application
function landingPageApp() {
  return {
    showModal: false,
    darkMode: false,
    form: {
      email: '',
      company: '',
      role: ''
    },
    stats: {
      waitlist: 2847,
      satisfaction: 94,
      productivity: 12
    },
    
    init() {
      // Initialize dark mode
      this.initDarkMode();
      
      // Track page visit
      if (typeof leadScoring !== 'undefined') {
        leadScoring.trackPageVisit();
      }
      
      // Initialize stats animation after DOM load
      this.$nextTick(() => {
        this.animateStats();
      });
      
      // Track visitor engagement
      this.trackEngagement();
    },
    
    initDarkMode() {
      // Check localStorage for dark mode preference
      const savedDarkMode = localStorage.getItem('darkMode');
      
      if (savedDarkMode !== null) {
        this.darkMode = savedDarkMode === 'true';
      } else {
        // Check system preference
        this.darkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      }
      
      // Watch for changes
      this.$watch('darkMode', (value) => {
        localStorage.setItem('darkMode', value);
        if (value) {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
      });
      
      // Apply initial state
      if (this.darkMode) {
        document.documentElement.classList.add('dark');
      }
    },
    
    requestAccess() {
      this.showModal = true;
      if (typeof leadScoring !== 'undefined') {
        leadScoring.trackAction('opened_access_modal', 10);
      }
    },
    
    submitAccessRequest() {
      // Validate form
      if (!this.form.email) {
        alert('Please enter your email');
        return;
      }
      
      // Track submission
      if (typeof leadScoring !== 'undefined') {
        leadScoring.trackSubmission({
          email: this.form.email,
          company: this.form.company,
          role: this.form.role
        });
        
        leadScoring.trackAction('submitted_access_request', 20);
      }
      
      // Show success message
      alert('Thank you! We\'ll be in touch soon with your early access invitation.');
      
      // Reset form and close modal
      this.form = {
        email: '',
        company: '',
        role: ''
      };
      this.showModal = false;
    },
    
    animateStats() {
      // Animate stats when they come into view
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            // Animate waitlist number
            this.animateNumber('waitlist', 0, 2847, 2000);
            
            // Animate satisfaction percentage
            this.animateNumber('satisfaction', 0, 94, 1500);
            
            // Unobserve after animation
            observer.unobserve(entry.target);
          }
        });
      });
      
      // Observe stats section
      const statsElement = document.querySelector('[x-text="stats.waitlist"]');
      if (statsElement) {
        observer.observe(statsElement.closest('section'));
      }
    },
    
    animateNumber(property, start, end, duration) {
      const startTime = performance.now();
      const range = end - start;
      
      const animate = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        
        this.stats[property] = Math.round(start + (range * easeOutQuart));
        
        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      };
      
      requestAnimationFrame(animate);
    },
    
    trackEngagement() {
      // Track scroll depth
      let maxScroll = 0;
      window.addEventListener('scroll', () => {
        const scrollPercentage = Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100);
        if (scrollPercentage > maxScroll) {
          maxScroll = scrollPercentage;
          
          // Track milestones
          if (maxScroll >= 25 && maxScroll < 50) {
            if (typeof leadScoring !== 'undefined') {
              leadScoring.trackAction('scrolled_25', 2);
            }
          } else if (maxScroll >= 50 && maxScroll < 75) {
            if (typeof leadScoring !== 'undefined') {
              leadScoring.trackAction('scrolled_50', 3);
            }
          } else if (maxScroll >= 75) {
            if (typeof leadScoring !== 'undefined') {
              leadScoring.trackAction('scrolled_75', 5);
            }
          }
        }
      });
      
      // Track time on page
      let timeOnPage = 0;
      setInterval(() => {
        timeOnPage++;
        
        // Track engagement milestones
        if (timeOnPage === 30) {
          if (typeof leadScoring !== 'undefined') {
            leadScoring.trackAction('engaged_30s', 5);
          }
        } else if (timeOnPage === 60) {
          if (typeof leadScoring !== 'undefined') {
            leadScoring.trackAction('engaged_60s', 10);
          }
        }
      }, 1000);
      
      // Track clicks on key elements
      document.addEventListener('click', (e) => {
        const trackableElement = e.target.closest('[data-track]');
        if (trackableElement) {
          const action = trackableElement.getAttribute('data-track');
          if (typeof leadScoring !== 'undefined') {
            leadScoring.trackAction(action, 3);
          }
        }
      });
    }
  };
}

// Initialize Alpine.js when DOM is loaded
document.addEventListener('alpine:init', () => {
  console.log('Alpine.js initialized');
});



        // Funcionalidades específicas do ChessMaster
        class ChessFeatures {
            constructor() {
                this.initChessAnimations();
                this.initGameModeSelection();
            }
            
            initChessAnimations() {
                // Animação das peças no preview
                const pieces = document.querySelectorAll('.chess-piece');
                pieces.forEach((piece, index) => {
                    piece.style.animationDelay = `${index * 0.5}s`;
                });
            }
            
            initGameModeSelection() {
                const gameModes = document.querySelectorAll('.game-mode-card');
                gameModes.forEach(mode => {
                    mode.addEventListener('click', function() {
                        // Destacar modo selecionado
                        gameModes.forEach(m => m.classList.remove('selected'));
                        this.classList.add('selected');
                        
                        // Adicionar ao lead scoring
                        if (window.leadScoring) {
                            window.leadScoring.updateScore('gameMode', 10);
                        }
                    });
                });
            }
        }
        
        // Inicializar funcionalidades de xadrez
        document.addEventListener('DOMContentLoaded', () => {
            new ChessFeatures();
            
            // Adicionar handler para o botão Jogar Agora da navegação
            const navPlayBtn = document.getElementById('nav-play');
            if (navPlayBtn) {
                navPlayBtn.addEventListener('click', function() {
                    // Reutilizar a mesma lógica do botão principal
                    const ctaPlay = document.getElementById('cta-play');
                    if (ctaPlay) {
                        ctaPlay.click();
                    }
                });
            }
        });
        