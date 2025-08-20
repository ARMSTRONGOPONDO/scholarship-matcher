
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

// Sample JSON data structure - In production, this would be loaded from your files
const mentalHealthData = {
    resources: [
        {
            "id": 1,
            "title": "Understanding Anxiety Disorders",
            "description": "Learn about different types of anxiety disorders, their symptoms, and evidence-based treatment approaches to manage anxiety effectively.",
            "type": "article",
            "category": "Articles",
            "image": "https://images.unsplash.com/photo-1491841550275-ad7854e35ca6?q=80",
            "rating": 4.8,
            "readTime": 12,
            "date": "2023-05-15"
        },
        {
            "id": 2,
            "title": "Mindfulness Meditation Guide",
            "description": "A 20-minute guided meditation session to help reduce stress and improve focus through mindfulness techniques.",
            "type": "video",
            "category": "Videos",
            "image": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80",
            "rating": 4.9,
            "duration": 21,
            "views": 12400
        },
        {
            "id": 3,
            "title": "Breaking the Stigma",
            "description": "Conversations with mental health experts about overcoming societal stigma around mental illness in everyday life.",
            "type": "podcast",
            "category": "Podcasts",
            "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80",
            "rating": 4.7,
            "duration": 48,
            "listens": 8200
        },
        {
            "id": 4,
            "title": "Coping with Depression",
            "description": "Practical strategies for managing depressive symptoms and improving mood through daily habits and cognitive techniques.",
            "type": "article",
            "category": "Articles",
            "image": "https://images.unsplash.com/photo-1584697964358-3e14ca57658b?q=80",
            "rating": 4.6,
            "readTime": 15,
            "date": "2023-04-22"
        }
    ],
    disorders: [
        {
            "id": 1,
            "name": "Depression",
            "description": "Persistent sadness, loss of interest, and low energy affecting daily life.",
            "symptoms": ["Low mood", "Loss of interest", "Fatigue", "Sleep disturbances"],
            "icon": "cloud"
        },
        {
            "id": 2,
            "name": "Anxiety Disorders",
            "description": "Excessive fear, worry, and physical symptoms like rapid heartbeat.",
            "symptoms": ["Excessive worry", "Restlessness", "Muscle tension", "Panic attacks"],
            "icon": "wind"
        },
        {
            "id": 3,
            "name": "Bipolar Disorder",
            "description": "Mood swings ranging from depressive lows to manic highs.",
            "symptoms": ["Mood swings", "Energy changes", "Sleep disturbances", "Risky behavior"],
            "icon": "balance-scale"
        },
        {
            "id": 4,
            "name": "PTSD",
            "description": "Persistent mental and emotional stress following a traumatic event.",
            "symptoms": ["Flashbacks", "Nightmares", "Hypervigilance", "Avoidance"],
            "icon": "puzzle-piece"
        },
        {
            "id": 5,
            "name": "Eating Disorders",
            "description": "Unhealthy eating habits and preoccupation with body weight.",
            "symptoms": ["Extreme dieting", "Binge eating", "Purging", "Body image issues"],
            "icon": "utensils"
        },
        {
            "id": 6,
            "name": "Substance Use",
            "description": "Harmful pattern of using substances like alcohol or drugs.",
            "symptoms": ["Cravings", "Withdrawal", "Tolerance", "Loss of control"],
            "icon": "prescription-bottle"
        }
    ],
    professionals: [
        {
            "id": 1,
            "name": "Dr. Sarah Johnson",
            "title": "Licensed Clinical Psychologist",
            "specialties": ["Depression", "Anxiety", "Trauma"],
            "location": "New York, NY",
            "image": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?q=80"
        },
        {
            "id": 2,
            "name": "Michael Rodriguez",
            "title": "Licensed Marriage & Family Therapist",
            "specialties": ["Relationships", "Family Issues", "Grief"],
            "location": "Los Angeles, CA",
            "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80"
        },
        {
            "id": 3,
            "name": "Dr. Aisha Patel",
            "title": "Clinical Social Worker",
            "specialties": ["Anxiety", "Stress", "Life Transitions"],
            "location": "Chicago, IL",
            "image": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?q=80"
        }
    ],
    crisis: [
        {
            "id": 1,
            "name": "Suicide & Crisis Lifeline",
            "number": "988",
            "description": "24/7 support for anyone in suicidal crisis or emotional distress"
        },
        {
            "id": 2,
            "name": "National Suicide Prevention Lifeline",
            "number": "1-800-273-TALK (8255)",
            "description": "Free and confidential support for people in distress"
        },
        {
            "id": 3,
            "name": "Substance Abuse Helpline",
            "number": "1-800-662-HELP (4357)",
            "description": "Treatment referral and information service"
        }
    ],
    stats: [
        {
            "id": 1,
            "value": "1 in 5",
            "description": "Adults experience mental illness each year"
        },
        {
            "id": 2,
            "value": "50%",
            "description": "Of mental health conditions begin by age 14"
        },
        {
            "id": 3,
            "value": "75%",
            "description": "Of mental illnesses are treatable with proper care"
        },
        {
            "id": 4,
            "value": "17.3M",
            "description": "US adults experienced at least one major depressive episode"
        }
    ]
};

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
            `<span class="specialty">${spec}</span>`
        ).join('');
        
        card.innerHTML = `
            <div class="therapist-img" style="background: url('${therapist.image}') center/cover;"></div>
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

// Filter resources by category
function filterResources(category) {
    if (category === 'all') {
        renderResources(mentalHealthData.resources);
        return;
    }
    
    const filtered = mentalHealthData.resources.filter(
        resource => resource.type === category
    );
    renderResources(filtered);
}

// Search functionality
function searchResources(query) {
    const lowerQuery = query.toLowerCase().trim();
    
    if (!lowerQuery) {
        renderResources(mentalHealthData.resources);
        return;
    }
    
    const results = mentalHealthData.resources.filter(resource => 
        resource.title.toLowerCase().includes(lowerQuery) || 
        resource.description.toLowerCase().includes(lowerQuery) ||
        resource.category.toLowerCase().includes(lowerQuery)
    );
    
    renderResources(results);
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
newsletterForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (emailInput.value) {
        alert(`Thank you for subscribing with: ${emailInput.value}`);
        emailInput.value = '';
    }
});

// Initialize the page with data
function initializePage() {
    // Simulate loading delay
    setTimeout(() => {
        renderResources(mentalHealthData.resources);
        renderDisorders(mentalHealthData.disorders);
        renderTherapists(mentalHealthData.professionals);
        renderCrisis(mentalHealthData.crisis);
        renderStats(mentalHealthData.stats);
    }, 1500);
}

// Start the application
initializePage();
