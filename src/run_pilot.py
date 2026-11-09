"""AI-assisted midterm component. See prompts/ and docs/AI_DISCLOSURE.md.
Deterministic replay of saved LLM outputs; no fresh model calls, no trained GCN.
Only visualization requires matplotlib. Data validation/export use stdlib.
"""
from __future__ import annotations
import argparse,collections,csv,html,json,math,pathlib,sys,textwrap,xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
TYPES=['population','design','intervention','duration','measurement','outcome','qualifier']
COLORS={'preserved':'#157F76','omitted':'#CA653C','study':'#20344C'}

def load_data(path):
    papers=json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    if not isinstance(papers,list) or not papers: raise ValueError('Expected nonempty paper list')
    paper_ids=set(); claim_ids=set()
    for p in papers:
        if p['id'] in paper_ids: raise ValueError('Duplicate paper ID')
        paper_ids.add(p['id'])
        if not p['abstract'].strip() or not p['summary'].strip(): raise ValueError('Empty input text')
        for c in p['claims']:
            if c['id'] in claim_ids: raise ValueError('Duplicate claim ID')
            claim_ids.add(c['id'])
            if c['type'] not in TYPES: raise ValueError('Unknown concept type')
            if c['status'] not in ('preserved','omitted'): raise ValueError('Unknown provisional label')
            if not c['source_anchor'] or c['source_anchor'] not in p['abstract']: raise ValueError('Unanchored source claim: '+c['id'])
            if c['status']=='preserved' and (not c['summary_evidence'] or c['summary_evidence'] not in p['summary']): raise ValueError('Unanchored preservation: '+c['id'])
            if c['status']=='omitted' and c['summary_evidence']: raise ValueError('Omitted claim has summary evidence')
    return papers

def graph(p,version):
    # A source-aligned graph of the selected audited information units, not an exhaustive medical KG.
    # Summary membership is the saved assistant alignment, not a learned model prediction.
    claims=[c for c in p['claims'] if version=='source' or c['status']=='preserved']
    nodes=[dict(id=p['id'],text=p['short'],type='study')]+[dict(id=c['id'],text=c['text'],type=c['type']) for c in claims]
    edges=[(p['id'],c['id'],'has_'+c['type']) for c in claims]
    interventions=[c for c in claims if c['type']=='intervention']
    if interventions:
        edges += [(interventions[0]['id'],c['id'],'assessed_for') for c in claims if c['type']=='outcome']
    return nodes,edges

def stats(nodes,edges):
    degree=collections.Counter({n['id']:0 for n in nodes})
    for a,b,_ in edges: degree[a]+=1; degree[b]+=1
    return dict(nodes=len(nodes),edges=len(edges),mean_total_degree=sum(degree.values())/len(nodes),degree_distribution=dict(sorted(collections.Counter(degree.values()).items())))

def graphml(nodes,edges,dest):
    ns='http://graphml.graphdrawing.org/xmlns';ET.register_namespace('',ns)
    root=ET.Element('{'+ns+'}graphml')
    for k in ['text','type']: ET.SubElement(root,'{'+ns+'}key',id=k,**{'for':'node','attr.name':k,'attr.type':'string'})
    ET.SubElement(root,'{'+ns+'}key',id='relation',**{'for':'edge','attr.name':'relation','attr.type':'string'})
    g=ET.SubElement(root,'{'+ns+'}graph',edgedefault='directed')
    for n in nodes:
        el=ET.SubElement(g,'{'+ns+'}node',id=n['id'])
        for k in ['text','type']: ET.SubElement(el,'{'+ns+'}data',key=k).text=n[k]
    for i,(a,b,r) in enumerate(edges):
        el=ET.SubElement(g,'{'+ns+'}edge',id=f'e{i}',source=a,target=b)
        ET.SubElement(el,'{'+ns+'}data',key='relation').text=r
    ET.ElementTree(root).write(dest,encoding='utf-8',xml_declaration=True)

def positions(p):
    pos={p['id']:(0,0)}
    for i,c in enumerate(p['claims']):
        theta=math.pi/2-2*math.pi*i/len(p['claims']);pos[c['id']]=(math.cos(theta),math.sin(theta))
    return pos

def plots(papers,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
    for p in papers:
        pos=positions(p); fig,axs=plt.subplots(1,2,figsize=(15,7.4))
        for ax,version in zip(axs,['source','summary']):
            nodes,edges=graph(p,version)
            for a,b,r in edges:
                ax.add_patch(FancyArrowPatch(pos[a],pos[b],arrowstyle='-|>',mutation_scale=12,color='#AEB9C5',linewidth=1.1,shrinkA=19,shrinkB=18,connectionstyle='arc3,rad=0.04'))
            ids={n['id'] for n in nodes}
            for n in nodes:
                x,y=pos[n['id']];ax.scatter(x,y,s=400 if n['type']=='study' else 250,c=COLORS['study'] if n['type']=='study' else COLORS['preserved'],zorder=3)
                label=p['short'] if n['type']=='study' else n['id'].split('_')[1]+': '+n['text']
                if n['type']=='study': ax.text(x,y-.12,label,ha='center',va='top',fontsize=10,weight='bold')
                else:
                    ax.text(x*1.14,y*1.14,'\n'.join(textwrap.wrap(label,22)),ha='left' if x>.1 else 'right' if x<-.1 else 'center',va='center',fontsize=9,color='#20344C')
            if version=='summary':
                for c in p['claims']:
                    if c['id'] not in ids:
                        x,y=pos[c['id']];ax.scatter(x,y,s=250,facecolors='none',edgecolors=COLORS['omitted'],linestyle='--',zorder=3)
                        ax.text(x*1.14,y*1.14,c['id'].split('_')[1]+' omitted',ha='left' if x>.1 else 'right' if x<-.1 else 'center',va='center',fontsize=9,color=COLORS['omitted'])
            ax.set(xlim=(-1.95,1.95),ylim=(-1.5,1.5));ax.set_aspect('equal');ax.axis('off')
            ax.set_title(('Source' if version=='source' else 'Summary')+' graph',fontsize=16,pad=20)
        fig.suptitle(p['short']+' • selected, source-aligned information units',fontsize=18,y=.98)
        fig.text(.5,.025,'Teal: represented unit. Orange outline: omitted source unit, shown only for comparison. AI-assisted annotations pending student review.',ha='center',fontsize=10)
        fig.tight_layout(rect=(0,.06,1,.94));fig.savefig(out/(p['id']+'_graph_comparison.png'),dpi=170);fig.savefig(out/(p['id']+'_graph_comparison.svg'));plt.close(fig)
    categories=[t for t in TYPES if any(c['type']==t for p in papers for c in p['claims'])]
    preserved=[sum(c['type']==t and c['status']=='preserved' for p in papers for c in p['claims']) for t in categories]
    omitted=[sum(c['type']==t and c['status']=='omitted' for p in papers for c in p['claims']) for t in categories]
    fig,ax=plt.subplots(figsize=(10,5.6));ax.barh(categories,preserved,color=COLORS['preserved'],label='Preserved');ax.barh(categories,omitted,left=preserved,color=COLORS['omitted'],label='Omitted')
    for i,(a,b) in enumerate(zip(preserved,omitted)):
        if a:ax.text(a/2,i,str(a),ha='center',va='center',color='white',weight='bold')
        if b:ax.text(a+b/2,i,str(b),ha='center',va='center',color='white',weight='bold')
    ax.set_xlabel('Selected information units');ax.set_title('Pilot coverage by information type');ax.invert_yaxis();ax.legend(loc='lower right');fig.tight_layout();fig.savefig(out/'coverage_by_type.png',dpi=170);fig.savefig(out/'coverage_by_type.svg');plt.close(fig)
    degrees=sorted({int(k) for p in papers for v in ['source','summary'] for k in stats(*graph(p,v))['degree_distribution']})
    fig,ax=plt.subplots(figsize=(10,5.5));width=.36
    for offset,v,col in [(-width/2,'source','#20344C'),(width/2,'summary','#157F76')]:
        counter=collections.Counter()
        for p in papers:counter.update(stats(*graph(p,v))['degree_distribution'])
        ax.bar([i+offset for i in range(len(degrees))],[counter[d] for d in degrees],width,label=v.title(),color=col)
    ax.set_xticks(range(len(degrees)),degrees);ax.set_xlabel('Total degree (in + out)');ax.set_ylabel('Number of nodes across three separate graphs');ax.legend();ax.set_title('Pilot degree distributions');fig.tight_layout();fig.savefig(out/'degree_distribution.png',dpi=170);plt.close(fig)

def interactive(papers,out):
    # Standalone SVG/HTML graph viewer. Source data is embedded and no CDN or network is needed.
    blocks=[]
    for p in papers:
        coords=positions(p);nodes,edges=graph(p,'source');svg=['<svg viewBox="0 0 1000 690" role="img" aria-label="Source graph colored by provisional summary coverage"><defs><marker id="arrow'+p['id']+'" markerWidth="8" markerHeight="8" refX="18" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#9daabb"/></marker></defs>']
        for a,b,r in edges:
            x,y=coords[a];xx,yy=coords[b];svg.append(f'<line x1="{500+x*285}" y1="{340-y*250}" x2="{500+xx*285}" y2="{340-yy*250}" stroke="#9daabb" marker-end="url(#arrow{p["id"]})"><title>{html.escape(r)}</title></line>')
        lookup={c['id']:c for c in p['claims']}
        for n in nodes:
            x,y=coords[n['id']];x=500+x*285;y=340-y*250;c=lookup.get(n['id']);status=c['status'] if c else 'study';tooltip=n['text']+(' — '+status+'; '+c['review_status'] if c else '')
            svg.append(f'<g tabindex="0"><circle cx="{x}" cy="{y}" r="21" fill="{COLORS[status]}"><title>{html.escape(tooltip)}</title></circle><text x="{x}" y="{y+5}" text-anchor="middle" fill="white" font-size="12">{n["id"].split("_")[-1]}</text>')
            lines=textwrap.wrap(n['text'],25)
            for i,l in enumerate(lines):svg.append(f'<text x="{x}" y="{y+42+i*15}" text-anchor="middle" font-size="12">{html.escape(l)}</text>')
            svg.append('</g>')
        svg.append('</svg>')
        blocks.append('<section id="'+p['id']+'"><h2>'+html.escape(p['short'])+'</h2><a href="'+p['url']+'">Original article</a>'+''.join(svg)+'<h3>Saved AI summary</h3><p>'+html.escape(p['summary'])+'</p></section>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Exercise and sleep omission pilot</title><style>body{font:17px system-ui;max-width:1100px;margin:30px auto;padding:0 25px;color:#20344c}svg{width:100%;height:auto}section{border-top:1px solid #ccd3db;margin-top:30px}a{color:#157f76}g:focus circle{stroke:black;stroke-width:4}nav a{margin-right:25px}</style><h1>Exercise and sleep omission pilot</h1><p>Three real abstracts. Saved AI-generated summaries and AI-assisted provisional annotations. No trained GCN or independent human validation.</p><p>Teal = preserved information unit. Orange = omitted. Hover or focus a node for detail.</p><nav>'''+''.join('<a href="#'+p['id']+'">'+p['short']+'</a>' for p in papers)+'</nav>'+''.join(blocks)+'</html>'
    (out/'interactive_graphs.html').write_text(page,encoding='utf-8')

def run(data,out,make_plots=True):
    papers=load_data(data);out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
    rows=[];table=[]
    for p in papers:
        row={'paper_id':p['id'],'study':p['short'],'selected_units':len(p['claims']),'preserved':sum(c['status']=='preserved' for c in p['claims']),'omitted':sum(c['status']=='omitted' for c in p['claims'])}
        for v in ['source','summary']:
            nodes,edges=graph(p,v);graphml(nodes,edges,out/(p['id']+'_'+v+'.graphml'))
            row[v+'_graph']=stats(nodes,edges)
        table.append(row)
        for c in p['claims']:rows.append({'paper_id':p['id'],**c,'reviewer_1':'','reviewer_2':'','adjudicated_label':''})
    totals={'papers':len(papers),'selected_units':len(rows),'preserved':sum(r['status']=='preserved' for r in rows),'omitted':sum(r['status']=='omitted' for r in rows)}
    result={'status':'Midterm feasibility pilot; AI-assisted labels; no trained model','totals':totals,'papers':table,'interpretation':'Counts describe selected information units in these saved summaries only. They are not model accuracy, clinical trust scores or population omission rates.'}
    (out/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    with (out/'annotation_review.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    with (out/'graph_statistics.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['paper_id','version','nodes','edges','mean_total_degree','degree_distribution'])
        for p in table:
            for v in ['source','summary']:
                s=p[v+'_graph'];w.writerow([p['paper_id'],v,s['nodes'],s['edges'],s['mean_total_degree'],json.dumps(s['degree_distribution'])])
    interactive(papers,out)
    if make_plots:plots(papers,out)
    report=['# Validation log','',f"PASS: {len(papers)} paper IDs and {len(rows)} claim IDs are unique.",'PASS: All source anchors occur in their stored abstracts.','PASS: All preserved units have matching summary evidence.','PASS: All graph endpoints refer to known nodes.','PASS: Statistics and coverage counts derived from the same saved input.','PENDING: Two students independently review claims and labels.','PENDING: Annotation agreement and adjudication.','PENDING: Full corpus, GCN and non-graph evaluation.','',result['interpretation']]
    (out/'validation_log.md').write_text('\n'.join(report),encoding='utf-8')
    print(json.dumps(totals));return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=pathlib.Path,default=ROOT/'data/pilot.json')
    parser.add_argument('--output',type=pathlib.Path,default=ROOT/'results')
    parser.add_argument('--no-plots',action='store_true',help='Run using only the Python standard library')
    args=parser.parse_args()
    try:run(args.data,args.output,not args.no_plots)
    except (ValueError,KeyError,FileNotFoundError) as e:parser.exit(1,'Validation failed: '+str(e)+'\n')
