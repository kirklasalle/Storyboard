import React, { useEffect, useState } from 'react';
import { Users, Mic, Eye, Film, BookOpen, ChevronDown, ChevronUp } from 'lucide-react';
import { API_BASE } from '../utils/api';

interface Character {
    id: string;
    name: string;
    role: string;
    description: string;
    age_range: string;
    wardrobe: string;
    visual_prompt: string;
    voice_id: string;
    voice_description: string;
    is_lead: boolean;
    scene_count: number;
    line_count: number;
}

interface Archetype {
    id: string;
    name: string;
    narrative_role: string;
    jungian_archetype: string;
    genre_type: string;
    visual_prompt: string;
    voice_id: string;
    voice_description: string;
    visual_style_notes: string;
    wardrobe_signature: string;
    usage_count: number;
}

interface LibraryStats {
    total_archetypes: number;
    by_role: Record<string, number>;
    by_genre_type: Record<string, number>;
    taxonomy: {
        narrative_roles: number;
        jungian_archetypes: number;
        production_tiers: number;
        genre_types: number;
        possible_combinations: number;
    };
    most_used: { name: string; usage: number }[];
}

const VOICE_COLORS: Record<string, string> = {
    alloy:   'bg-slate-500/20 text-slate-300 border-slate-500/30',
    echo:    'bg-blue-500/20 text-blue-300 border-blue-500/30',
    fable:   'bg-amber-500/20 text-amber-300 border-amber-500/30',
    onyx:    'bg-purple-500/20 text-purple-300 border-purple-500/30',
    nova:    'bg-rose-500/20 text-rose-300 border-rose-500/30',
    shimmer: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
};

const ROLE_COLORS: Record<string, string> = {
    protagonist: 'text-indigo-400',
    antagonist:  'text-rose-400',
    deuteragonist: 'text-violet-400',
    mentor:      'text-amber-400',
    love_interest: 'text-pink-400',
};

interface CharacterLibraryViewProps {
    projectId: string | null;
}

export const CharacterLibraryView: React.FC<CharacterLibraryViewProps> = ({ projectId }) => {
    const [projectChars, setProjectChars] = useState<Character[]>([]);
    const [archetypes, setArchetypes] = useState<Archetype[]>([]);
    const [stats, setStats] = useState<LibraryStats | null>(null);
    const [activeTab, setActiveTab] = useState<'project' | 'library' | 'stats'>('project');
    const [expandedChar, setExpandedChar] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            setLoading(true);
            try {
                const [arcResp, statsResp] = await Promise.all([
                    fetch(`${API_BASE}/characters/library?limit=50`),
                    fetch(`${API_BASE}/characters/library/stats`),
                ]);
                if (arcResp.ok) setArchetypes(await arcResp.json());
                if (statsResp.ok) setStats(await statsResp.json());

                if (projectId) {
                    const cResp = await fetch(`${API_BASE}/projects/${projectId}/characters`);
                    if (cResp.ok) setProjectChars(await cResp.json());
                }
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [projectId]);

    const VoiceBadge = ({ voiceId }: { voiceId: string }) => (
        <span className={`text-[9px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full border ${VOICE_COLORS[voiceId] || VOICE_COLORS.alloy}`}>
            {voiceId}
        </span>
    );

    const renderProjectChars = () => (
        <div className="space-y-4">
            {!projectId && (
                <div className="text-center py-16 text-slate-600">
                    <Users className="w-12 h-12 mx-auto mb-4 opacity-30" />
                    <p className="font-medium">Create and analyze a project to see its character profiles.</p>
                </div>
            )}
            {projectId && projectChars.length === 0 && !loading && (
                <div className="text-center py-16 text-slate-600">
                    <Users className="w-12 h-12 mx-auto mb-4 opacity-30" />
                    <p className="font-medium">No characters extracted yet.</p>
                    <p className="text-sm mt-1">Run analysis on a script to populate character profiles.</p>
                </div>
            )}
            {projectChars.map(c => (
                <div key={c.id} className="glass-morphism rounded-2xl border border-white/5 overflow-hidden">
                    <button
                        className="w-full p-5 text-left flex items-center justify-between hover:bg-white/2 transition-colors"
                        onClick={() => setExpandedChar(expandedChar === c.id ? null : c.id)}
                    >
                        <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 flex items-center justify-center">
                                <span className="text-indigo-400 font-black text-sm">{c.name[0]}</span>
                            </div>
                            <div>
                                <div className="flex items-center gap-2">
                                    <span className="font-bold text-white">{c.name}</span>
                                    {c.is_lead && (
                                        <span className="text-[9px] font-black uppercase tracking-widest px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-400">LEAD</span>
                                    )}
                                    <VoiceBadge voiceId={c.voice_id || 'alloy'} />
                                </div>
                                <div className="flex items-center gap-3 mt-0.5">
                                    <span className={`text-[10px] font-bold uppercase tracking-wider ${ROLE_COLORS[c.role] || 'text-slate-500'}`}>{c.role?.replace('_', ' ')}</span>
                                    {c.age_range && <span className="text-[10px] text-slate-600">{c.age_range}</span>}
                                    <span className="text-[10px] text-slate-600">{c.scene_count} scene{c.scene_count !== 1 ? 's' : ''}</span>
                                </div>
                            </div>
                        </div>
                        {expandedChar === c.id ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
                    </button>

                    {expandedChar === c.id && (
                        <div className="px-5 pb-5 space-y-4 border-t border-white/5 pt-4">
                            {c.description && (
                                <div>
                                    <p className="text-[9px] font-bold uppercase tracking-widest text-slate-600 mb-1 flex items-center gap-1.5"><Eye className="w-3 h-3" /> Visual Profile</p>
                                    <p className="text-xs text-slate-300 leading-relaxed">{c.description}</p>
                                </div>
                            )}
                            {c.wardrobe && (
                                <div>
                                    <p className="text-[9px] font-bold uppercase tracking-widest text-slate-600 mb-1">Wardrobe</p>
                                    <p className="text-xs text-slate-400">{c.wardrobe}</p>
                                </div>
                            )}
                            {c.visual_prompt && (
                                <div>
                                    <p className="text-[9px] font-bold uppercase tracking-widest text-slate-600 mb-1 flex items-center gap-1.5"><Film className="w-3 h-3" /> Image Generation Prompt</p>
                                    <p className="text-[10px] text-indigo-300 font-mono bg-indigo-500/5 border border-indigo-500/10 rounded-lg px-3 py-2">{c.visual_prompt}</p>
                                </div>
                            )}
                            {c.voice_description && (
                                <div>
                                    <p className="text-[9px] font-bold uppercase tracking-widest text-slate-600 mb-1 flex items-center gap-1.5"><Mic className="w-3 h-3" /> Voice / Read-Through</p>
                                    <div className="flex items-center gap-2">
                                        <VoiceBadge voiceId={c.voice_id || 'alloy'} />
                                        <p className="text-xs text-slate-400 italic">{c.voice_description}</p>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            ))}
        </div>
    );

    const renderLibrary = () => (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {archetypes.map(a => (
                <div key={a.id} className="glass-morphism rounded-2xl border border-white/5 p-5 space-y-3">
                    <div className="flex items-start justify-between gap-2">
                        <div>
                            <p className="font-bold text-sm text-white">{a.name}</p>
                            <div className="flex items-center gap-2 mt-1 flex-wrap">
                                <span className={`text-[9px] font-bold uppercase tracking-widest ${ROLE_COLORS[a.narrative_role] || 'text-slate-500'}`}>{a.narrative_role?.replace('_', ' ')}</span>
                                {a.genre_type && <span className="text-[9px] text-slate-600 uppercase tracking-wider">{a.genre_type?.replace('_', ' ')}</span>}
                                <VoiceBadge voiceId={a.voice_id || 'alloy'} />
                            </div>
                        </div>
                        {a.usage_count > 0 && (
                            <span className="text-[9px] text-slate-600 shrink-0">×{a.usage_count}</span>
                        )}
                    </div>
                    {a.visual_prompt && (
                        <p className="text-[10px] text-slate-400 leading-relaxed italic">"{a.visual_prompt}"</p>
                    )}
                    {a.wardrobe_signature && (
                        <p className="text-[9px] text-slate-600">{a.wardrobe_signature}</p>
                    )}
                </div>
            ))}
        </div>
    );

    const renderStats = () => (
        <div className="space-y-6">
            {stats && (
                <>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {[
                            { label: 'Total Archetypes', value: stats.total_archetypes },
                            { label: 'Narrative Roles', value: stats.taxonomy?.narrative_roles },
                            { label: 'Jungian Types', value: stats.taxonomy?.jungian_archetypes },
                            { label: 'Type Combinations', value: stats.taxonomy?.possible_combinations?.toLocaleString() },
                        ].map(item => (
                            <div key={item.label} className="glass-morphism rounded-2xl border border-white/5 p-5 text-center">
                                <p className="text-2xl font-black text-indigo-400">{item.value}</p>
                                <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">{item.label}</p>
                            </div>
                        ))}
                    </div>
                    <div className="glass-morphism rounded-2xl border border-white/5 p-5">
                        <p className="text-[9px] font-bold uppercase tracking-widest text-slate-600 mb-4">Most Used Archetypes</p>
                        <div className="space-y-2">
                            {stats.most_used?.map(m => (
                                <div key={m.name} className="flex items-center justify-between">
                                    <span className="text-xs text-slate-300">{m.name}</span>
                                    <span className="text-xs text-slate-600">×{m.usage}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </>
            )}
        </div>
    );

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="flex items-center gap-3">
                <div className="p-3 bg-indigo-500/10 rounded-2xl">
                    <Users className="w-8 h-8 text-indigo-500" />
                </div>
                <div>
                    <h3 className="text-3xl font-black tracking-tight">Character Library</h3>
                    <p className="text-slate-400">Visual profiles, voice casting, and growing archetype database</p>
                </div>
            </div>

            <div className="flex items-center gap-1 bg-slate-900/50 rounded-xl p-1 border border-white/5 w-fit">
                {([['project', 'Project Characters'], ['library', 'Archetype Library'], ['stats', 'Library Stats']] as const).map(([tab, label]) => (
                    <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${activeTab === tab ? 'bg-indigo-600 text-white' : 'text-slate-500 hover:text-white'}`}
                    >
                        {label}
                    </button>
                ))}
            </div>

            {loading ? (
                <div className="text-center py-16 text-slate-600">Loading character data...</div>
            ) : (
                <>
                    {activeTab === 'project' && renderProjectChars()}
                    {activeTab === 'library' && renderLibrary()}
                    {activeTab === 'stats' && renderStats()}
                </>
            )}
        </div>
    );
};
