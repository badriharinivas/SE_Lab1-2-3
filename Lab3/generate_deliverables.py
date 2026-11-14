from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Arc, FancyArrowPatch, Rectangle
from matplotlib import rcParams
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.units import inch

OUT = Path(__file__).parent

# Component diagram: a modular layered monolith with a single transactional store.
fig, ax = plt.subplots(figsize=(15, 9), dpi=180)
fig.patch.set_facecolor('#f7f9fc')
ax.set_facecolor('#f7f9fc')
ax.set_xlim(0, 15); ax.set_ylim(0, 9.3); ax.axis('off')

layers = [
    (0.35, 0.65, 2.35, 7.35, 'PRESENTATION', '#eaf2ff'),
    (3.05, 0.65, 2.75, 7.35, 'APPLICATION', '#eaf8f4'),
    (6.15, 0.65, 4.05, 7.35, 'DOMAIN MODULES', '#fff6e8'),
    (10.55, 0.65, 4.05, 7.35, 'INFRASTRUCTURE', '#f2edff'),
]
for x,y,w,h,label,color in layers:
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.03,rounding_size=0.12',
                                linewidth=1.2,edgecolor='#c7d0dc',facecolor=color,zorder=0))
    ax.text(x+0.16,y+h-0.28,label,fontsize=10,fontweight='bold',color='#425466',va='top')

nodes = {
 'portal': (1.525,5.30,1.72,1.02,'Borrower / Lender\nWeb Portal','<<component>>'),
 'api': (4.425,5.30,2.00,1.02,'Application API\n& Access Control','<<component>>'),
 'loan': (8.175,5.30,2.25,1.02,'Loan & Funding\nManager','<<component>>'),
 'risk': (8.175,7.00,2.25,1.02,'Credit Risk\nAssessment Engine','<<component>>'),
 'repay': (8.175,2.55,2.25,1.02,'Repayment & EMI\nManager','<<component>>'),
 'db': (12.575,5.30,2.35,1.02,'Relational Data Store\n(ACID transactions)','<<component>>'),
 'notify': (12.575,2.55,2.35,1.02,'Notification\nManager','<<component>>'),
}
colors_map={'portal':'#ffffff','api':'#ffffff','loan':'#ffffff','risk':'#ffffff','repay':'#ffffff','db':'#ffffff','notify':'#ffffff'}
for key,(cx,cy,w,h,title,stereo) in nodes.items():
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2),w,h,boxstyle='round,pad=0.05,rounding_size=0.08',
                                linewidth=1.7,edgecolor='#274060',facecolor=colors_map[key],zorder=4))
    ax.text(cx,cy+0.20,stereo,ha='center',va='center',fontsize=8,color='#607286',zorder=5)
    ax.text(cx,cy-0.08,title,ha='center',va='center',fontsize=10,fontweight='bold',color='#172b4d',zorder=5)

# Interface connections. Each is a dependency from a required socket to a provided ball.
# Labels are placed manually to keep the UML view readable.
edges=[
 ('portal','api','Platform API\n(HTTPS / JSON)',(2.98,5.67)),
 ('api','loan','Loan request / funding API',(6.55,5.63)),
 ('api','risk','Risk assessment API',(6.42,6.70)),
 ('api','repay','Repayment & schedule API',(6.47,3.57)),
 ('loan','risk','Risk rating lookup',(8.80,6.53)),
 ('loan','repay','Create repayment schedule',(9.34,4.00)),
 ('loan','db','Loan / funding repository',(10.48,5.75)),
 ('risk','db','Profile / history query',(10.50,6.90)),
 ('repay','db','ACID payment / EMI records',(10.48,3.22)),
 ('repay','notify','Overdue event interface',(11.24,2.93)),
]
# endpoints approach the boxes; curved arrows distinguish parallel and crossing flows.
for i,(a,b,label,lpos) in enumerate(edges):
    ax1,ay1,aw,ah,*_=nodes[a]; bx,by,bw,bh,*_=nodes[b]
    dx=bx-ax1; dy=by-ay1
    # Use edges from outside the rectangles; curved lines avoid obscuring labels and nodes.
    start=(ax1+(aw/2 if dx>=0 else -aw/2), ay1 + max(-ah/2+0.10,min(ah/2-0.10,dy*0.12)))
    end=(bx-(bw/2 if dx>=0 else -bw/2), by - max(-bh/2+0.10,min(bh/2-0.10,dy*0.12)))
    rad=[0.0,0.08,-0.08,0.12,-0.12,0.05,-0.04,0.04,-0.08,0.0][i]
    patch=FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=12,linewidth=1.35,
                          color='#50647a',connectionstyle=f'arc3,rad={rad}',zorder=2)
    ax.add_patch(patch)
    # socket at requiring end; ball at providing end, placed just outside each component.
    sx,sy=start; ex,ey=end
    ax.add_patch(Arc((sx,sy),0.22,0.22,theta1=90,theta2=270,linewidth=1.5,color='#1d4e89',zorder=6))
    ax.add_patch(Circle((ex,ey),0.075,facecolor='white',edgecolor='#1d4e89',linewidth=1.5,zorder=6))
    ax.text(lpos[0],lpos[1],label,ha='center',va='center',fontsize=8,
            color='#26384a',bbox=dict(boxstyle='round,pad=0.22',facecolor='#f7f9fc',edgecolor='none',alpha=0.94),zorder=6)

# Legend / scope note
ax.add_patch(Circle((0.75,0.32),0.075,facecolor='white',edgecolor='#1d4e89',linewidth=1.5))
ax.text(0.90,0.32,'provided interface (ball)',va='center',fontsize=8,color='#34495e')
ax.add_patch(Arc((3.10,0.32),0.22,0.22,theta1=90,theta2=270,linewidth=1.5,color='#1d4e89'))
ax.text(3.28,0.32,'required interface (socket)',va='center',fontsize=8,color='#34495e')
ax.text(7.0,0.32,'Solid connectors show calls/events; the modules are deployed together.',va='center',fontsize=8,color='#526579')
ax.text(7.5,8.88,'Micro-Lending & Peer Credit Risk Assessor',ha='center',fontsize=17,fontweight='bold',color='#172b4d')
ax.text(7.5,8.55,'UML Component Diagram  |  Modular layered monolith',ha='center',fontsize=10,color='#526579')
fig.savefig(OUT/'Component_Diagram.png',bbox_inches='tight',facecolor=fig.get_facecolor())
fig.savefig(OUT/'Component_Diagram.pdf',bbox_inches='tight',facecolor=fig.get_facecolor())
plt.close(fig)

# One-page written justification.
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCenter',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=17,leading=20,textColor=colors.HexColor('#17324d'),alignment=TA_CENTER,spaceAfter=5))
styles.add(ParagraphStyle(name='Subtitle',parent=styles['Normal'],fontSize=9,leading=12,textColor=colors.HexColor('#526579'),alignment=TA_CENTER,spaceAfter=12))
styles.add(ParagraphStyle(name='Section',parent=styles['Heading2'],fontSize=10.5,leading=13,textColor=colors.HexColor('#1d4e89'),spaceBefore=7,spaceAfter=3))
styles.add(ParagraphStyle(name='BodyLab',parent=styles['BodyText'],fontSize=9.2,leading=12.3,textColor=colors.HexColor('#26384a'),spaceAfter=5))
styles.add(ParagraphStyle(name='SmallLab',parent=styles['BodyText'],fontSize=8.2,leading=10.5,textColor=colors.HexColor('#26384a')))

doc=SimpleDocTemplate(str(OUT/'Architecture_Justification.pdf'),pagesize=letter,
    rightMargin=0.62*inch,leftMargin=0.62*inch,topMargin=0.48*inch,bottomMargin=0.48*inch,
    title='Architecture Justification - Micro-Lending Peer Credit Risk Assessor',author='Lab 3')
story=[]
story.append(Paragraph('Architecture Selection: Micro-Lending &amp; Peer Credit Risk Assessor',styles['TitleCenter']))
story.append(Paragraph('Lab 3 — Component Modelling &amp; Architectural Pattern Selection',styles['Subtitle']))
story.append(Paragraph('We chose a <b>modular layered monolith</b> for the Micro-Lending &amp; Peer Credit Risk Assessor.',styles['BodyLab']))
story.append(Paragraph('Architectural style analysis',styles['Section']))
data=[
 [Paragraph('<b>Style</b>',styles['SmallLab']),Paragraph('<b>Fit for this scenario</b>',styles['SmallLab'])],
 [Paragraph('Layered',styles['SmallLab']),Paragraph('Clear separation of portal, application, domain, and data responsibilities; can keep repayment writes in one ACID transaction. Modular code keeps the prototype understandable.',styles['SmallLab'])],
 [Paragraph('Microservices',styles['SmallLab']),Paragraph('Independent scaling is possible, but network calls, deployment overhead, and distributed transaction consistency add avoidable complexity for a single-tenant prototype with a 50-concurrent-request target.',styles['SmallLab'])],
 [Paragraph('Client-server',styles['SmallLab']),Paragraph('Simple centralized deployment, but by itself it does not define module boundaries and risks concentrating all responsibilities in one server component.',styles['SmallLab'])],
]
t=Table(data,colWidths=[1.15*inch,5.95*inch],repeatRows=1)
t.setStyle(TableStyle([
 ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eaf2ff')),('TEXTCOLOR',(0,0),(-1,-1),colors.HexColor('#26384a')),
 ('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#cbd5e1')),('VALIGN',(0,0),(-1,-1),'TOP'),
 ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(t)
story.append(Paragraph('Two scenario-specific reasons',styles['Section']))
story.append(Paragraph('<b>1. Repayment correctness:</b> Lab 1 requires repayment records and loan balances to remain consistent, with duplicate payments prevented. Keeping the repayment manager and relational store in one application boundary makes ACID transactions straightforward. <b>2. Appropriate scale and scope:</b> the stated target is 50 concurrent risk assessments, and the project is a single-tenant academic prototype. A modular layered application provides enough separation without the operational and cross-service coordination cost of microservices.',styles['BodyLab']))
story.append(Paragraph('Security advantage',styles['Section']))
story.append(Paragraph('The Application API provides one controlled entry point for borrower and lender actions. Central authentication/authorization checks can enforce role-based access (borrowers see their own profile; lenders see only information needed for funding decisions), while TLS protects traffic and the data layer stays behind the application boundary.',styles['BodyLab']))
story.append(Paragraph('Performance benefit',styles['Section']))
story.append(Paragraph('Risk scoring and internal module calls run in-process, avoiding extra network hops. A relational store with indexed borrower, loan, and installment keys supports profile/history lookups and the repayment schedule queries needed to meet the Lab 1 target of a 2-second risk response for 95% of requests under normal load.',styles['BodyLab']))
story.append(Spacer(1,4))
story.append(Paragraph('Assumption: the modules are logical components in one deployable application; payment collection rails and regulatory/KYC integrations remain outside the Lab 1 prototype scope.',styles['SmallLab']))
doc.build(story)

print('Created:')
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name != Path(__file__).name:
        print(f'{p.name} ({p.stat().st_size:,} bytes)')

