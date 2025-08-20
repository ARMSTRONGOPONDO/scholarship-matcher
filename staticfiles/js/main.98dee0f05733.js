
// DOM Elements
const themeToggle = document.getElementById('themeToggle');
const resourcesContainer = document.getElementById('resourcesContainer');
const conditionsContainer = document.getElementById('conditionsContainer');
const therapistsContainer = document.getElementById('therapistsContainer');
const crisisContainer = document.getElementById('crisisContainer');
const statsContainer = document.getElementById('statsContainer');
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const categories = document.querySelectorAll('.category');
const newsletterForm = document.getElementById('newsletterForm');
const emailInput = document.getElementById('emailInput');

// API URLs
const API_BASE = '/api';
const RESOURCES_URL = `${API_BASE}/resources/`;
const DISORDERS_URL = `${API_BASE}/disorders/`;
const THERAPISTS_URL = `${API_BASE}/therapists/`;
const CRISIS_URL = `${API_BASE}/crisis-resources/`;
const STATS_URL = `${API_BASE}/statistics/`;
const NEWSLETTER_URL = `${API_BASE}/newsletter/subscribe/`;
const SEARCH_URL = `${API_BASE}/search/`;
const PODCASTS_URL = `${API_BASE}/podcasts/`;
const PODCAST_SEARCH_URL = `${API_BASE}/podcasts/search/`;

// Theme Toggle
themeToggle.addEventListener('click', () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
    themeToggle.innerHTML = isDark ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-sun"></i>';
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
});

// Load saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeToggle.innerHTML = savedTheme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
}

// Function to fetch data from API
async function fetchAPI(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data.results || data; // Handle pagination results
    } catch (error) {
        console.error('Error fetching data:', error);
        return [];
    }
}

// Function to render resources
function renderResources(resources) {
    resourcesContainer.innerHTML = '';
    
    if (resources.length === 0) {
        resourcesContainer.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search fa-3x"></i>
                <h3>No resources found</h3>
                <p>Try adjusting your search or filter criteria</p>
            </div>
        `;
        return;
    }
    
    resources.forEach(resource => {
        const card = document.createElement('div');
        card.className = 'resource-card';
        
        // Determine meta content based on resource type
        let metaContent = '';
        if (resource.type === 'article') {
            metaContent = `
                <div class="meta-item"><i class="far fa-clock"></i> ${resource.read_time} min read</div>
                <div class="meta-item"><i class="far fa-calendar"></i> ${resource.date_published}</div>
            `;
        } else if (resource.type === 'video') {
            metaContent = `
                <div class="meta-item"><i class="far fa-clock"></i> ${resource.duration} min</div>
                <div class="meta-item"><i class="fas fa-eye"></i> ${resource.views.toLocaleString()} views</div>
            `;
        } else if (resource.type === 'podcast') {
            metaContent = `
                <div class="meta-item"><i class="far fa-clock"></i> ${resource.duration} min</div>
                <div class="meta-item"><i class="fas fa-headphones"></i> ${resource.listens.toLocaleString()} listens</div>
            `;
        }
        
        // Use image_url if available, otherwise use a default image
        const imageUrl = resource.image_url || (resource.image ? resource.image : 'https://via.placeholder.com/400x250?text=Mental+Health+Resource');
        
        card.innerHTML = `
            <div class="card-img" style="background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url('${imageUrl}') center/cover;">
                <div class="resource-rating"><i class="fas fa-star"></i> ${resource.rating}</div>
            </div>
            <div class="card-content">
                <span class="resource-type">${resource.category_name}</span>
                <h3 class="resource-title">${resource.title}</h3>
                <p class="resource-description">${resource.description}</p>
                <div class="resource-meta">
                    ${metaContent}
                </div>
                <div class="card-footer">
                    <a href="#" class="read-more" data-id="${resource.id}">
                        <i class="${resource.type === 'article' ? 'fas fa-book-open' : resource.type === 'video' ? 'fas fa-play' : 'fas fa-headphones'}"></i>
                        ${resource.type === 'article' ? 'Read More' : resource.type === 'video' ? 'Watch Now' : 'Listen Now'}
                    </a>
                    <button class="save-btn" data-id="${resource.id}"><i class="far fa-bookmark"></i></button>
                </div>
            </div>
        `;
        resourcesContainer.appendChild(card);
    });
    
    // Add event listeners to save buttons
    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // If user is logged in (token exists in localStorage)
            const token = localStorage.getItem('token');
            if (token) {
                saveResource(this.dataset.id, token);
            } else {
                alert('Please log in to save resources.');
                // Redirect to login page or show login modal
            }
        });
    });
}
                <p>Try adjusting your search or filter criteria</p>
            </div>
        `;
        return;
    }
    
    resources.forEach(resource => {
        const card = document.createElement('div');
        card.className = 'resource-card';
        
        // Determine meta content based on resource type
        let metaContent = '';
        if (resource.type === 'article') {
            metaContent = `
                <div class="meta-item"><i class="far fa-clock"></i> ${resource.readTime} min read</div>
                <div class="meta-item"><i class="far fa-calendar"></i> ${resource.date}</div>
            `;
        } else if (resource.type === 'video') {
            metaContent = `
                <div class="meta-item"><i class="far fa-clock"></i> ${resource.duration} min</div>
                <div class="meta-item"><i class="fas fa-eye"></i> ${resource.views.toLocaleString()} views</div>
            `;
        } else if (resource.type === 'podcast') {
            metaContent = `
                <div class="meta-item"><i class="far fa-clock"></i> ${resource.duration} min</div>
                <div class="meta-item"><i class="fas fa-headphones"></i> ${resource.listens.toLocaleString()} listens</div>
            `;
        }
        
        card.innerHTML = `
            <div class="card-img" style="background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url('${resource.image}') center/cover;">
                <div class="resource-rating"><i class="fas fa-star"></i> ${resource.rating}</div>
            </div>
            <div class="card-content">
                <span class="resource-type">${resource.category}</span>
                <h3 class="resource-title">${resource.title}</h3>
                <p class="resource-description">${resource.description}</p>
                <div class="resource-meta">
                    ${metaContent}
                </div>
                <div class="card-footer">
                    <a href="#" class="read-more">
                        <i class="${resource.type === 'article' ? 'fas fa-book-open' : resource.type === 'video' ? 'fas fa-play' : 'fas fa-headphones'}"></i>
                        ${resource.type === 'article' ? 'Read More' : resource.type === 'video' ? 'Watch Now' : 'Listen Now'}
                    </a>
                    <button class="save-btn"><i class="far fa-bookmark"></i></button>
                </div>
            </div>
        `;
        resourcesContainer.appendChild(card);
    });
}

// Function to render disorders
function renderDisorders(disorders) {
    conditionsContainer.innerHTML = '';
    
    disorders.forEach(disorder => {
        const card = document.createElement('div');
        card.className = 'condition-card';
        card.innerHTML = `
            <i class="fas fa-${disorder.icon}"></i>
            <h3>${disorder.name}</h3>
            <p>${disorder.description}</p>
        `;
        conditionsContainer.appendChild(card);
    });
}

// Function to render therapists
function renderTherapists(therapists) {
    therapistsContainer.innerHTML = '';
    
    therapists.forEach(therapist => {
        const card = document.createElement('div');
        card.className = 'therapist-card';
        
        // Create specialties string
        const specialties = therapist.specialties.map(spec => 
            `<span class="specialty">${spec.name}</span>`
        ).join('');
        
        // Use image_url if available, otherwise use a default image
        const imageUrl = therapist.image_url || (therapist.image ? therapist.image : 'https://via.placeholder.com/400x400?text=Therapist');
        
        card.innerHTML = `
            <div class="therapist-img" style="background: url('${imageUrl}') center/cover;"></div>
            <div class="therapist-info">
                <h3>${therapist.name}</h3>
                <p>${therapist.title}</p>
                <div class="therapist-specialties">
                    ${specialties}
                </div>
                <p><i class="fas fa-map-marker-alt"></i> ${therapist.location}</p>
                <div class="therapist-contact">
                    <a href="#" class="contact-btn profile-btn"><i class="fas fa-user"></i> Profile</a>
                    <a href="#" class="contact-btn book-btn"><i class="fas fa-calendar"></i> Book</a>
                </div>
            </div>
        `;
        therapistsContainer.appendChild(card);
    });
}

// Function to render crisis resources
function renderCrisis(crisisResources) {
    crisisContainer.innerHTML = '';
    
    crisisResources.forEach(crisis => {
        const item = document.createElement('div');
        item.className = 'crisis-number';
        item.innerHTML = `
            <i class="fas fa-phone-alt"></i>
            <p>${crisis.number}</p>
            <span>${crisis.name}</span>
        `;
        crisisContainer.appendChild(item);
    });
}

// Function to render stats
function renderStats(stats) {
    statsContainer.innerHTML = '';
    
    stats.forEach(stat => {
        const item = document.createElement('div');
        item.className = 'stat-item';
        item.innerHTML = `
            <div class="stat-number">${stat.value}</div>
            <p>${stat.description}</p>
        `;
        statsContainer.appendChild(item);
    });
}
}

// Filter resources by category
async function filterResources(category) {
    try {
        let url = RESOURCES_URL;
        if (category !== 'all') {
            url += `?type=${category}`;
        }
        const resources = await fetchAPI(url);
        renderResources(resources);
        
        // If podcast category is selected, also fetch podcasts from Podcast Index API
        if (category === 'podcast') {
            // Show loading indicator
            const loadMoreBtn = document.createElement('div');
            loadMoreBtn.className = 'load-more-btn';
            loadMoreBtn.innerHTML = '<div class="spinner"></div><span>Loading podcast episodes...</span>';
            resourcesContainer.appendChild(loadMoreBtn);
            
            // Fetch podcasts
            const podcasts = await fetchAPI(PODCASTS_URL + '?category=recent');
            
            // Remove loading indicator
            resourcesContainer.removeChild(loadMoreBtn);
            
            // Add podcasts to resources
            if (podcasts && podcasts.length > 0) {
                renderPodcasts(podcasts);
            }
        }
    } catch (error) {
        console.error('Error filtering resources:', error);
    }
}

// Render podcasts from the Podcast Index API
function renderPodcasts(podcasts) {
    // Create a section title for the podcasts
    const podcastsTitle = document.createElement('div');
    podcastsTitle.className = 'podcasts-title';
    podcastsTitle.innerHTML = '<h3>Latest Mental Health Podcast Episodes</h3><p>Fresh insights from mental health experts</p>';
    resourcesContainer.appendChild(podcastsTitle);
    
    // Create a container for podcast episodes
    const podcastsContainer = document.createElement('div');
    podcastsContainer.className = 'podcasts-container';
    
    podcasts.forEach(podcast => {
        const card = document.createElement('div');
        card.className = 'podcast-card';
        
        // Format the duration
        const duration = podcast.duration;
        let formattedDuration;
        if (duration > 60) {
            formattedDuration = Math.floor(duration / 60) + 'h ' + (duration % 60) + 'm';
        } else {
            formattedDuration = duration + 'm';
        }
        
        // Use podcast image or a default
        const imageUrl = podcast.image || 'https://via.placeholder.com/400x400?text=Podcast';
        
        card.innerHTML = '<div class="podcast-img" style="background-image: url(\'' + imageUrl + '\')"></div>' +
            '<div class="podcast-content">' +
            '<h4>' + podcast.title + '</h4>' +
            '<p class="podcast-show">' + (podcast.podcast_title || 'Mental Health Podcast') + '</p>' +
            '<p class="podcast-description">' + podcast.description.substring(0, 120) + '...</p>' +
            '<div class="podcast-meta">' +
            '<span><i class="far fa-clock"></i> ' + formattedDuration + '</span>' +
            '</div>' +
            '<div class="podcast-actions">' +
            '<a href="' + podcast.enclosure_url + '" target="_blank" class="podcast-play-btn">' +
            '<i class="fas fa-play"></i> Play Episode' +
            '</a>' +
            '</div>' +
            '</div>';
        
        podcastsContainer.appendChild(card);
    });
    
    resourcesContainer.appendChild(podcastsContainer);
    
    // Add a button to explore more podcasts
    const exploreMoreBtn = document.createElement('div');
    exploreMoreBtn.className = 'explore-more-btn';
    exploreMoreBtn.innerHTML = '<a href="#" id="explorePodcasts">Explore More Mental Health Podcasts</a>';
    resourcesContainer.appendChild(exploreMoreBtn);
    
    // Add event listener to the explore more button
    document.getElementById('explorePodcasts').addEventListener('click', async (e) => {
        e.preventDefault();
        
        // Show loading indicator
        exploreMoreBtn.innerHTML = '<div class="spinner"></div> <span>Loading podcasts...</span>';
        
        try {
            // Fetch popular podcasts
            const popularPodcasts = await fetchAPI(PODCASTS_URL + '?category=popular');
            
            // Clear current resources
            resourcesContainer.innerHTML = '';
            
            // Create a title
            const title = document.createElement('div');
            title.className = 'section-title-container';
            title.innerHTML = '<h2>Mental Health Podcasts</h2>' +
                '<p>Discover expert insights, personal stories, and evidence-based resources</p>' +
                '<div class="podcast-filter">' +
                '<button class="podcast-filter-btn active" data-type="popular">Popular Shows</button>' +
                '<button class="podcast-filter-btn" data-type="trending">Trending Episodes</button>' +
                '<button class="podcast-filter-btn" data-type="recent">Recent Episodes</button>' +
                '</div>';
            resourcesContainer.appendChild(title);
            
            // Create a container for podcasts
            const podcastGrid = document.createElement('div');
            podcastGrid.className = 'podcast-grid';
            resourcesContainer.appendChild(podcastGrid);
            
            // Render popular podcasts
            renderPodcastShows(popularPodcasts, podcastGrid);
            
            // Add event listeners to filter buttons
            document.querySelectorAll('.podcast-filter-btn').forEach(btn => {
                btn.addEventListener('click', async () => {
                    // Update active class
                    document.querySelectorAll('.podcast-filter-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    
                    // Show loading
                    podcastGrid.innerHTML = '<div class="spinner large-spinner"></div>';
                    
                    // Fetch podcasts based on type
                    const type = btn.dataset.type;
                    const podcastData = await fetchAPI(PODCASTS_URL + '?category=' + type);
                    
                    // Render based on type
                    if (type === 'popular') {
                        renderPodcastShows(podcastData, podcastGrid);
                    } else {
                        renderPodcastEpisodes(podcastData, podcastGrid);
                    }
                });
            });
            
        } catch (error) {
            console.error('Error fetching podcasts:', error);
            exploreMoreBtn.innerHTML = 'Error loading podcasts. Try again.';
        }
    });
}

// Render podcast shows
function renderPodcastShows(podcasts, container) {
    container.innerHTML = '';
    
    if (!podcasts || podcasts.length === 0) {
        container.innerHTML = '<div class="no-results">No podcasts found</div>';
        return;
    }
    
    podcasts.forEach(podcast => {
        const card = document.createElement('div');
        card.className = 'podcast-show-card';
        
        // Use podcast image or a default
        const imageUrl = podcast.image || 'https://via.placeholder.com/300x300?text=Podcast';
        
        card.innerHTML = '<div class="podcast-show-img" style="background-image: url(\'' + imageUrl + '\')"></div>' +
            '<div class="podcast-show-content">' +
            '<h3>' + podcast.title + '</h3>' +
            '<p class="podcast-show-author">By ' + (podcast.author || 'Unknown') + '</p>' +
            '<p class="podcast-show-description">' + podcast.description.substring(0, 100) + '...</p>' +
            '<div class="podcast-show-meta">' +
            '<span><i class="fas fa-microphone-alt"></i> ' + (podcast.episode_count || 0) + ' episodes</span>' +
            '</div>' +
            '<a href="' + podcast.feed_url + '" target="_blank" class="podcast-show-btn">' +
            '<i class="fas fa-podcast"></i> Subscribe' +
            '</a>' +
            '</div>';
        
        container.appendChild(card);
    });
}

// Render podcast episodes
function renderPodcastEpisodes(episodes, container) {
    container.innerHTML = '';
    
    if (!episodes || episodes.length === 0) {
        container.innerHTML = '<div class="no-results">No episodes found</div>';
        return;
    }
    
    episodes.forEach(episode => {
        const card = document.createElement('div');
        card.className = 'podcast-episode-card';
        
        // Format the duration
        const duration = episode.duration;
        let formattedDuration;
        if (duration > 60) {
            formattedDuration = Math.floor(duration / 60) + 'h ' + (duration % 60) + 'm';
        } else {
            formattedDuration = duration + 'm';
        }
            
        // Use episode image or a default
        const imageUrl = episode.image || 'https://via.placeholder.com/300x300?text=Episode';
        
        card.innerHTML = '<div class="podcast-episode-img" style="background-image: url(\'' + imageUrl + '\')">' +
            '<div class="podcast-play-overlay">' +
            '<i class="fas fa-play-circle"></i>' +
            '</div>' +
            '</div>' +
            '<div class="podcast-episode-content">' +
            '<h3>' + episode.title + '</h3>' +
            '<p class="podcast-episode-show">' + (episode.podcast_title || 'Mental Health Podcast') + '</p>' +
            '<p class="podcast-episode-description">' + episode.description.substring(0, 100) + '...</p>' +
            '<div class="podcast-episode-meta">' +
            '<span><i class="far fa-clock"></i> ' + formattedDuration + '</span>' +
            '</div>' +
            '<audio controls class="podcast-audio-player">' +
            '<source src="' + episode.enclosure_url + '" type="' + (episode.enclosure_type || 'audio/mpeg') + '">' +
            'Your browser does not support the audio element.' +
            '</audio>' +
            '</div>';
        
        container.appendChild(card);
        
        // Add click event to the play overlay
        const playOverlay = card.querySelector('.podcast-play-overlay');
        const audioPlayer = card.querySelector('.podcast-audio-player');
        
        playOverlay.addEventListener('click', () => {
            audioPlayer.play();
            playOverlay.style.opacity = '0';
        });
    });
}

// Search functionality
async function searchResources(query) {
    try {
        if (!query.trim()) {
            const resources = await fetchAPI(RESOURCES_URL);
            renderResources(resources);
            return;
        }
        
        const searchData = await fetchAPI(SEARCH_URL + '?q=' + encodeURIComponent(query));
        renderResources(searchData.resources || []);
    } catch (error) {
        console.error('Error searching:', error);
    }
}

// Save a resource to user profile
async function saveResource(resourceId, token) {
    try {
        const response = await fetch(RESOURCES_URL + resourceId + '/save/', {
            method: 'POST',
            headers: {
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('HTTP error! Status: ' + response.status);
        }
        
        const data = await response.json();
        alert(data.message);
    } catch (error) {
        console.error('Error saving resource:', error);
        alert('Error saving resource. Please try again.');
    }
}

// Newsletter subscription
async function subscribeNewsletter(email) {
    try {
        const response = await fetch(NEWSLETTER_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        if (!response.ok) {
            throw new Error('HTTP error! Status: ' + response.status);
        }
        
        const data = await response.json();
        alert(data.message);
        return true;
    } catch (error) {
        console.error('Error subscribing to newsletter:', error);
        alert('Error subscribing to newsletter. Please try again.');
        return false;
    }
}

// Event Listeners
searchButton.addEventListener('click', () => {
    searchResources(searchInput.value);
});

searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchResources(searchInput.value);
    }
});

categories.forEach(category => {
    category.addEventListener('click', () => {
        // Remove active class from all categories
        categories.forEach(cat => cat.classList.remove('active'));
        
        // Add active class to clicked category
        category.classList.add('active');
        
        // Filter resources
        filterResources(category.dataset.category);
    });
});

// Newsletter form submission
newsletterForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (emailInput.value) {
        const success = await subscribeNewsletter(emailInput.value);
        if (success) {
            emailInput.value = '';
        }
    }
});

// Initialize the page with data
async function initializePage() {
    try {
        // Show loading indicators
        resourcesContainer.innerHTML = '<div class="data-loading"><div class="spinner"></div><p>Loading mental health resources...</p></div>';
        conditionsContainer.innerHTML = '<div class="data-loading"><div class="spinner"></div><p>Loading mental health disorders...</p></div>';
        therapistsContainer.innerHTML = '<div class="data-loading"><div class="spinner"></div><p>Loading therapist information...</p></div>';
        crisisContainer.innerHTML = '<div class="data-loading"><div class="spinner"></div><p>Loading crisis resources...</p></div>';
        statsContainer.innerHTML = '<div class="data-loading"><div class="spinner"></div><p>Loading mental health statistics...</p></div>';
        
        // Fetch data from APIs in parallel
        const [resources, disorders, therapists, crisisResources, stats] = await Promise.all([
            fetchAPI(RESOURCES_URL),
            fetchAPI(DISORDERS_URL),
            fetchAPI(THERAPISTS_URL),
            fetchAPI(CRISIS_URL),
            fetchAPI(STATS_URL)
        ]);
        
        // Render data
        renderResources(resources);
        renderDisorders(disorders);
        renderTherapists(therapists);
        renderCrisis(crisisResources);
        renderStats(stats);
    } catch (error) {
        console.error('Error initializing page:', error);
    }
}

// Start the application
initializePage();
