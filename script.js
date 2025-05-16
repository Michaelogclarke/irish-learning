    let flashcards = [];
        let currentCardIndex = 0;
        let showingEnglish = false;
        let filteredFlashcards = [];
        let selectedCategories = new Set(); // second option
        let selectedTypes = new Set(["word", "sentence"]); // could be the issue

        // Fisher-Yates shuffle algorithm
        function shuffleArray(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        }

        async function loadFlashcards() {
            const response = await fetch('/api/flashcards');
            flashcards = await response.json();
            filteredFlashcards = [...flashcards];
            shuffleArray(filteredFlashcards);
            
            // Get unique categories
            const categories = [...new Set(flashcards.map(card => card.category))].sort();
            
            // Create checkboxes for each category
            const categoryCheckboxes = document.getElementById('categoryCheckboxes');
            categoryCheckboxes.innerHTML = '';
            
            categories.forEach(category => {
                const id = `category-${category.replace(/\s+/g, '-').toLowerCase()}`;
                const div = document.createElement('div');
                const checkboxHtml = `
                    <input type="checkbox" id="${id}" value="${category}" class="category-checkbox" checked>
                    <label for="${id}" class="category-label">
                        <div class="checkbox-custom"></div>
                        <span>${category}</span>
                    </label>
                `;
                div.innerHTML = checkboxHtml;
                categoryCheckboxes.appendChild(div);
                selectedCategories.add(category);
            });
            
            // Add event listeners for category checkboxes
            document.querySelectorAll('.category-checkbox').forEach(checkbox => {
                checkbox.addEventListener('change', () => {
                    if (checkbox.checked) {
                        selectedCategories.add(checkbox.value);
                    } else {
                        selectedCategories.delete(checkbox.value);
                    }
                    filterFlashcards();
                });
            });
            
            // Add event listeners for type checkboxes
            document.querySelectorAll('.type-checkbox').forEach(checkbox => {
                checkbox.addEventListener('change', () => {
                    if (checkbox.checked) {
                        selectedTypes.add(checkbox.value);
                    } else {
                        selectedTypes.delete(checkbox.value);
                    }
                    filterFlashcards();
                });
            });
            
            updateCard();
        }

        function filterFlashcards() {
            if (selectedCategories.size === 0 || selectedTypes.size === 0) {
                filteredFlashcards = [];
                // Show a message in the card when no categories or types are selected
                const frontContent = document.querySelector('.flashcard-front .card-content');
                const backContent = document.querySelector('.flashcard-back .card-content');
                
                let message = "No cards available";
                let instruction = "Please select at least one category";
                
                if (selectedTypes.size === 0) {
                    instruction = "Please select at least one content type (Words/Sentences)";
                }
                if (selectedCategories.size === 0 && selectedTypes.size === 0) {
                    instruction = "Please select at least one category and content type";
                }
                
                frontContent.innerHTML = `
                    <p class="text-xl sm:text-2xl font-semibold mb-2 text-red-600">${message}</p>
                    <p class="text-sm text-gray-600">${instruction}</p>
                `;
                
                backContent.innerHTML = `
                    <p class="text-xl sm:text-2xl font-semibold mb-2 text-red-600">${message}</p>
                    <p class="text-sm text-gray-600">${instruction}</p>
                `;
                
                // Hide the progress indicator when no categories are selected
                document.getElementById('progress').textContent = '0/0';
                return;
            } else {
                filteredFlashcards = flashcards.filter(card => 
                    selectedCategories.has(card.category) && 
                    (card.type ? selectedTypes.has(card.type) : true) // Handle cards that might not have a type field
                );
                shuffleArray(filteredFlashcards);
            }
            
            currentCardIndex = 0;
            updateCard();
        }

        function updateCard() {
            if (filteredFlashcards.length === 0) {
                // Handle empty filtered results
                const frontContent = document.querySelector('.flashcard-front .card-content');
                const backContent = document.querySelector('.flashcard-back .card-content');
                
                frontContent.innerHTML = `
                    <p class="text-xl sm:text-2xl font-semibold mb-2 text-red-600">No cards available</p>
                    <p class="text-sm text-gray-600">Please select at least one category</p>
                `;
                
                backContent.innerHTML = `
                    <p class="text-xl sm:text-2xl font-semibold mb-2 text-red-600">No cards available</p>
                    <p class="text-sm text-gray-600">Please select at least one category</p>
                `;
                
                // Update progress to show 0/0
                document.getElementById('progress').textContent = '0/0';
                return;
            }
            
            const currentCard = filteredFlashcards[currentCardIndex];
            
            // Reset the card content to normal display
            const frontContent = document.querySelector('.flashcard-front .card-content');
            const backContent = document.querySelector('.flashcard-back .card-content');
            
            frontContent.innerHTML = `
                <p id="cardTextFront" class="text-2xl sm:text-3xl font-semibold mb-2 sm:mb-4 text-green-800 font-irish"></p>
                <p id="categoryFront" class="text-xs sm:text-sm text-green-600 font-medium"></p>
            `;
            
            backContent.innerHTML = `
                <p id="cardTextBack" class="text-2xl sm:text-3xl font-semibold mb-2 sm:mb-4 text-green-800 font-irish"></p>
                <p id="categoryBack" class="text-xs sm:text-sm text-green-600 font-medium"></p>
            `;
            
            document.getElementById('cardTextFront').textContent = currentCard.irish;
            document.getElementById('categoryFront').textContent = currentCard.category;
            
            document.getElementById('cardTextBack').textContent = currentCard.english;
            document.getElementById('categoryBack').textContent = currentCard.category;
            
            // Reset card to front if it was flipped
            if (showingEnglish) {
                document.getElementById('currentCard').classList.remove('flipped');
                showingEnglish = false;
            }
            
            updateProgress();
        }

        function updateProgress() {
            const progressText = document.getElementById('progress');
            progressText.textContent = `${currentCardIndex + 1}/${filteredFlashcards.length}`;
        }

        let scores = {
            current_streak: 0,
            best_streak: 0,
            total_correct: 0,
            total_attempts: 0
        };

        async function loadScores() {
            const response = await fetch('/api/score');
            scores = await response.json();
            updateScoreDisplay();
        }

        function updateScoreDisplay() {
            document.getElementById('currentStreak').textContent = scores.current_streak;
            document.getElementById('bestStreak').textContent = scores.best_streak;
            
            const successRate = scores.total_attempts > 0 
                ? Math.round((scores.total_correct / scores.total_attempts) * 100) 
                : 0;
            
            document.getElementById('successRate').textContent = `${successRate}%`;
            
            // Add animation effect
            const streakElement = document.getElementById('currentStreak');
            streakElement.classList.add('score-increase');
            setTimeout(() => {
                streakElement.classList.remove('score-increase');
            }, 500);
        }

        document.getElementById('flipBtn').addEventListener('click', () => {
            const currentCard = document.getElementById('currentCard');
            currentCard.classList.toggle('flipped');
            showingEnglish = !showingEnglish;
        });

        async function submitAnswer(correct) {
            try {
                const response = await fetch('/api/score', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ correct }),
                });
                
                if (!response.ok) {
                    throw new Error('Failed to update score');
                }
                
                scores = await response.json();
                updateScoreDisplay();
                
                // Move to next card
                currentCardIndex = (currentCardIndex + 1) % filteredFlashcards.length;
                updateCard();
            } catch (error) {
                console.error('Error updating score:', error);
            }
        }

        document.getElementById('beginBtn').addEventListener('click', async () => {
            await Promise.all([loadFlashcards(), loadScores()]);
            document.getElementById('startScreen').classList.add('hidden');
            document.getElementById('practiceScreen').classList.add('visible');
        });

        document.getElementById('correctBtn').addEventListener('click', () => {
            document.getElementById('correctBtn').classList.add('scale-110', 'opacity-75');
            setTimeout(() => {
                document.getElementById('correctBtn').classList.remove('scale-110', 'opacity-75');
            }, 200);
            submitAnswer(true);
        });

        document.getElementById('incorrectBtn').addEventListener('click', () => {
            document.getElementById('incorrectBtn').classList.add('scale-110', 'opacity-75');
            setTimeout(() => {
                document.getElementById('incorrectBtn').classList.remove('scale-110', 'opacity-75');
            }, 200);
            submitAnswer(false);
        });

        // Side menu controls
        document.getElementById('openSideMenu').addEventListener('click', () => {
            document.querySelector('.side-menu').classList.add('open');
            document.querySelector('.side-menu-overlay').classList.add('active');
        });

        document.getElementById('closeSideMenu').addEventListener('click', () => {
            document.querySelector('.side-menu').classList.remove('open');
            document.querySelector('.side-menu-overlay').classList.remove('active');
        });

        document.querySelector('.side-menu-overlay').addEventListener('click', () => {
            document.querySelector('.side-menu').classList.remove('open');
            document.querySelector('.side-menu-overlay').classList.remove('active');
        });

        document.getElementById('selectAllCategories').addEventListener('click', () => {
            document.querySelectorAll('.category-checkbox').forEach(checkbox => {
                checkbox.checked = true;
                selectedCategories.add(checkbox.value);
            });
            filterFlashcards();
        });

        document.getElementById('deselectAllCategories').addEventListener('click', () => {
            document.querySelectorAll('.category-checkbox').forEach(checkbox => {
                checkbox.checked = false;
                selectedCategories.delete(checkbox.value);
            });
            filterFlashcards();
        });

