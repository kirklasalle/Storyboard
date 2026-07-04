import { useState, useEffect } from 'react'
import { Layout, Clapperboard, Settings, Database, Wand2, Plus, Bug, Copy, X } from 'lucide-react'
import { ScriptUploader } from './components/ScriptUploader'
import { Configuration } from './components/Configuration'
import { StoryboardGallery } from './components/StoryboardGallery'
import { API_BASE } from './utils/api'

function App() {
    const [view, setView] = useState<'home' | 'config' | 'upload' | 'gallery'>('home');
    const [projectId, setProjectId] = useState<string | null>(null);
    const [frames, setFrames] = useState<any[]>([]);
    const [config, setConfig] = useState<any>(null);

    useEffect(() => {
        const loadConfig = async () => {
            try {
                const resp = await fetch(`${API_BASE}/providers/config`);
                if (resp.ok) {
                    const data = await resp.json();
                    if (data) setConfig(data);
                }
            } catch (e) {
                console.error('Failed to load initial config', e);
            }
        };
        loadConfig();
    }, []);

    const handleCreateProject = async () => {
        try {
            const resp = await fetch(`${API_BASE}/projects`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: 'New Project', description: 'Generated Project' })
            });
            const data = await resp.json();
            setProjectId(data.id);
            setView('upload');
        } catch (e) {
            console.error(e);
            // Fallback for demo if backend is not running
            setProjectId('demo-id-' + Math.random().toString(36).substr(2, 9));
            setView('upload');
        }
    };

    const handleUploadSuccess = (id: string) => {
        setView('gallery');
    };

    const handleConfigSave = (newConfig: any) => {
        setConfig(newConfig);
    };

    // Global Debug State
    const [showDebugPanel, setShowDebugPanel] = useState(false);
    const [globalErrors, setGlobalErrors] = useState<string[]>([]);

    useEffect(() => {
        // Capture global errors
        const errorHandler = (e: ErrorEvent) => {
            setGlobalErrors(prev => [...prev, `${new Date().toLocaleTimeString()}: ${e.message}`].slice(-20));
        };
        window.addEventListener('error', errorHandler);
        return () => window.removeEventListener('error', errorHandler);
    }, []);

    const copyDebugInfo = () => {
        const info = {
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            currentView: view,
            projectId,
            config,
            backendUrl: 'http://127.0.0.1:8000',
            errors: globalErrors,
            localStorage: Object.keys(localStorage)
        };
        navigator.clipboard.writeText(JSON.stringify(info, null, 2));
        alert('Debug info copied to clipboard!');
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-50 flex flex-col selection:bg-indigo-500/30">
            <header className="border-b border-white/5 bg-slate-900/50 backdrop-blur-xl sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
                    <button onClick={() => setView('home')} className="flex items-center gap-2 hover:opacity-80 transition-opacity">
                        <Clapperboard className="w-8 h-8 text-indigo-500" />
                        <span className="text-xl font-bold tracking-tight">Storyboard AI</span>
                    </button>
                    <nav className="flex items-center gap-8">
                        <div className="has-tooltip">
                            <span className="tooltip">Manage and view your storyboard projects</span>
                            <button
                                onClick={() => setView('home')}
                                className={`text-sm font-medium transition-colors ${view === 'home' || view === 'gallery' || view === 'upload' ? 'text-white' : 'text-slate-500 hover:text-white'}`}
                            >
                                Projects
                            </button>
                        </div>
                        <div className="has-tooltip">
                            <span className="tooltip">Setup API keys and local AI models</span>
                            <button
                                onClick={() => setView('config')}
                                className={`text-sm font-medium transition-colors ${view === 'config' ? 'text-white' : 'text-slate-500 hover:text-white'}`}
                            >
                                Configuration
                            </button>
                        </div>
                    </nav>
                </div>
            </header>

            <main className="flex-1 max-w-7xl mx-auto px-4 py-12 w-full">
                {view === 'home' && (
                    <div className="text-center space-y-8 py-20">
                        <div className="space-y-4">
                            <h1 className="text-6xl font-black tracking-tight bg-gradient-to-b from-white to-slate-500 bg-clip-text text-transparent">
                                Directed by Intelligence.
                            </h1>
                            <p className="text-slate-400 text-xl max-w-2xl mx-auto leading-relaxed">
                                Transform your screenplay into high-impact storyboards.
                                Our AI analyzes intensity peaks and character consistency to build your visual vision.
                            </p>
                        </div>
                        <div className="flex items-center justify-center gap-4 pt-4">
                            <div className="has-tooltip">
                                <span className="tooltip">Initiate a new AI-assisted storyboard analysis</span>
                                <button
                                    onClick={handleCreateProject}
                                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 rounded-2xl font-bold transition-all shadow-2xl shadow-indigo-500/20 flex items-center gap-3 scale-110"
                                >
                                    <Plus className="w-6 h-6" />
                                    <span>Create New Storyboard</span>
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {view === 'upload' && projectId && (
                    <ScriptUploader projectId={projectId} onUploadSuccess={handleUploadSuccess} />
                )}

                {view === 'config' && (
                    <Configuration onSave={handleConfigSave} />
                )}

                {view === 'gallery' && projectId && (
                    <StoryboardGallery projectId={projectId} config={config} />
                )}
            </main>

            <footer className="border-t border-white/5 py-10">
                <div className="max-w-7xl mx-auto px-4 space-y-6">
                    {/* Philosophy quote */}
                    <div className="text-center py-4 border-b border-white/5">
                        <blockquote className="text-slate-500 text-sm italic leading-relaxed">
                            &ldquo;Every element is used because the story demands it &mdash; not as a syntax exercise.&rdquo;
                        </blockquote>
                        <cite className="text-[10px] font-bold uppercase tracking-widest text-indigo-500/60 mt-2 block not-italic">
                            — ACS4.6 &nbsp;&middot;&nbsp; Anthropic Claude Sonnet 4.6
                        </cite>
                    </div>
                    <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                        <div className="flex items-center gap-2 grayscale opacity-50">
                            <Clapperboard className="w-5 h-5" />
                            <span className="font-bold">Storyboard AI</span>
                        </div>
                        <div className="text-slate-600 text-xs">
                            Professional Grade Storyboarding &nbsp;&middot;&nbsp; Governed by Kirk LaSalle&rsquo;s 10 Laws
                        </div>
                        <div className="text-slate-700 text-xs">
                            &copy; {new Date().getFullYear()} Storyboard AI
                        </div>
                    </div>
                </div>
            </footer>

            {/* Floating Debug Button */}
            <button
                onClick={copyDebugInfo}
                title="Copy Debug Info"
                className="fixed bottom-6 right-6 p-4 bg-rose-600 hover:bg-rose-700 rounded-full shadow-2xl transition-all z-50 flex items-center gap-2 group"
            >
                <Bug className="w-6 h-6 text-white" />
                <span className="hidden group-hover:inline text-white text-sm font-bold">Copy Debug</span>
            </button>

            {/* Error Toast (if any) */}
            {globalErrors.length > 0 && (
                <div className="fixed bottom-24 right-6 bg-rose-500/90 text-white p-4 rounded-xl shadow-lg max-w-sm text-sm z-50">
                    <div className="font-bold mb-2">Recent Errors</div>
                    <div className="space-y-1 max-h-32 overflow-y-auto text-xs">
                        {globalErrors.slice(-5).map((err, i) => (
                            <div key={i} className="opacity-80">{err}</div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}

export default App
